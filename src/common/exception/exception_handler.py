#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from uvicorn.protocols.http.h11_impl import STATUS_PHRASES
from typing import Any, Dict, Union

from src.common.exception.errors import BaseExceptionMixin
from src.common.response.response_code import CustomResponseCode, StandardResponseCode
from src.common.response.response_schema import response_base
from src.common.schema import CUSTOM_VALIDATION_ERROR_MESSAGES

from src.core.settings import settings
from src.utils.serializers import MsgSpecJSONResponse
from src.utils.trace_id import get_request_trace_id


class ExceptionHandler:
    def __init__(self):
        # Initialize any common resources if needed
        pass

    def _get_http_status_code(self, code: Union[int, StandardResponseCode]) -> int:
        """
        Ensures a valid HTTP status code is returned.
        Converts StandardResponseCode enum to its integer value if necessary.
        """
        if isinstance(code, StandardResponseCode):
            code = code.value

        try:
            # Check if it's a known HTTP status code
            STATUS_PHRASES[code]
            return code
        except KeyError:
            # Fallback to a generic bad request or internal server error if unknown
            return StandardResponseCode.HTTP_400.value

    def _prepare_error_content(self, 
                                code: Union[int, StandardResponseCode], 
                                msg: str, 
                                data: Any = None, 
                                dev_data: Any = None
                            ) -> Dict[str, Any]:
        """
        Prepares the content dictionary for the JSON response based on environment.
        `dev_data` is used only in development environment.
        """
        if settings.ENVIRONMENT == 'dev':
            return {
                'code': code.value if isinstance(code, StandardResponseCode) else code,
                'msg': msg,
                'data': dev_data if dev_data is not None else data,
            }
        else:
            # Assuming CustomResponseCode.HTTP_400 is a generic client error for prod
            # And CustomResponseCode.HTTP_500 for server errors
            response_code = CustomResponseCode.HTTP_500 if code >= 500 else CustomResponseCode.HTTP_400
            res = response_base.fail(res=response_code)
            return res.model_dump()


    async def _handle_validation_errors(self, request: Request, exc: Union[RequestValidationError, ValidationError]):
        """
        Consolidated handler for both FastAPI and Pydantic validation exceptions.
        """
        errors_details = []
        for error in exc.errors():
            processed_error = error.copy() # Work on a copy to avoid modifying original
            custom_message = CUSTOM_VALIDATION_ERROR_MESSAGES.get(processed_error['type'])
            
            if custom_message:
                ctx = processed_error.get('ctx')
                if not ctx:
                    processed_error['msg'] = custom_message
                else:
                    try:
                        processed_error['msg'] = custom_message.format(**ctx)
                    except KeyError:
                        # Fallback if format string doesn't match ctx keys
                        processed_error['msg'] = custom_message
                    
                    ctx_error = ctx.get('error')
                    if ctx_error and isinstance(ctx_error, Exception):
                        # Ensure error is a string representation, often used in JSON
                        processed_error['ctx']['error'] = str(ctx_error).replace("'", '"')
            errors_details.append(processed_error)

        # Determine primary message
        first_error = errors_details[0]
        if first_error.get('type') == 'json_invalid':
            message = 'Failed to parse JSON data'
        else:
            field = str(first_error.get('loc')[-1])
            error_msg = first_error.get('msg')
            message = f'{field} {error_msg}, input: {first_error.get("input")}' if settings.ENVIRONMENT == 'dev' else error_msg
        
        msg_for_response = f'Invalid request parameters: {message}'

        content = self._prepare_error_content(
            code=StandardResponseCode.HTTP_422,
            msg=msg_for_response,
            data=None, # `data` for production is None, `dev_data` will be errors_details
            dev_data={'errors': errors_details}
        )
        request.state.__request_validation_exception__ = content
        content.update(trace_id=get_request_trace_id(request))
        return MsgSpecJSONResponse(status_code=StandardResponseCode.HTTP_422.value, content=content)


    def register(self, app: FastAPI):
        # Store a reference to the instance so handlers can call its methods
        # This is safe because `exception_handler` is a module-level singleton instance
        self_instance = self 

        @app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            """Handle HTTP exceptions."""
            content = self_instance._prepare_error_content(
                code=exc.status_code,
                msg=exc.detail,
                data=None, # No data for prod, `exc.detail` is msg
                dev_data=None # No extra dev data needed here
            )
            request.state.__request_http_exception__ = content
            content.update(trace_id=get_request_trace_id(request))
            return MsgSpecJSONResponse(
                status_code=self_instance._get_http_status_code(exc.status_code),
                content=content,
                headers=exc.headers,
            )

        @app.exception_handler(RequestValidationError)
        async def fastapi_validation_exception_handler(request: Request, exc: RequestValidationError):
            """Handle FastAPI validation exceptions."""
            return await self_instance._handle_validation_errors(request, exc)

        @app.exception_handler(ValidationError)
        async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
            """Handle Pydantic validation exceptions."""
            return await self_instance._handle_validation_errors(request, exc)

        @app.exception_handler(AssertionError)
        async def assertion_error_handler(request: Request, exc: AssertionError):
            """Handle assertion errors."""
            msg = str(exc.__str__() if exc.args else exc.__doc__ or "Assertion failed")
            content = self_instance._prepare_error_content(
                code=StandardResponseCode.HTTP_500,
                msg=msg,
                data=None,
                dev_data=None
            )
            request.state.__request_assertion_error__ = content
            content.update(trace_id=get_request_trace_id(request))
            return MsgSpecJSONResponse(
                status_code=StandardResponseCode.HTTP_500.value,
                content=content,
            )

        @app.exception_handler(BaseExceptionMixin)
        async def custom_exception_handler(request: Request, exc: BaseExceptionMixin):
            """Handle custom exceptions derived from BaseExceptionMixin."""
            content = self_instance._prepare_error_content(
                code=exc.code,
                msg=str(exc.msg), # Ensure msg is string
                data=exc.data if exc.data else None,
                dev_data=exc.data if exc.data else None # In this case, dev/prod data might be same if `data` is meant for both
            )
            request.state.__request_custom_exception__ = content
            content.update(trace_id=get_request_trace_id(request))
            return MsgSpecJSONResponse(
                status_code=self_instance._get_http_status_code(exc.code),
                content=content,
                background=exc.background,
            )

        @app.exception_handler(Exception)
        async def all_unknown_exception_handler(request: Request, exc: Exception):
            """Handle all unknown exceptions."""
            msg = str(exc)
            content = self_instance._prepare_error_content(
                code=StandardResponseCode.HTTP_500,
                msg=msg,
                data=None,
                dev_data=None # No extra dev data for generic
            )
            request.state.__request_all_unknown_exception__ = content
            content.update(trace_id=get_request_trace_id(request))
            return MsgSpecJSONResponse(
                status_code=StandardResponseCode.HTTP_500.value,
                content=content,
            )

        if settings.MIDDLEWARE_CORS:
            # Note: Handling CORS specifically in an exception handler for 500s
            # is typically done in very specific scenarios or as a workaround.
            # Standard CORS Middleware usually handles headers for *all* responses.
            @app.exception_handler(StandardResponseCode.HTTP_500)
            async def cors_custom_code_500_exception_handler(request: Request, exc: Exception):
                """
                Handle CORS custom 500 exceptions.

                `Related issue <https://github.com/encode/starlette/issues/1175>`_
                `Solution <https://github.com/fastapi/fastapi/discussions/7847#discussioncomment-5144709>`_
                """
                if isinstance(exc, BaseExceptionMixin):
                    content = self_instance._prepare_error_content(
                        code=exc.code,
                        msg=exc.msg,
                        data=exc.data,
                        dev_data=exc.data # Same as custom exception
                    )
                    status_code = self_instance._get_http_status_code(exc.code)
                    background = exc.background
                else:
                    # For non-BaseExceptionMixin 500s (e.g., generic Exception caught by this)
                    content = self_instance._prepare_error_content(
                        code=StandardResponseCode.HTTP_500,
                        msg=str(exc),
                        data=None,
                        dev_data=None
                    )
                    status_code = StandardResponseCode.HTTP_500.value
                    background = None

                request.state.__request_cors_500_exception__ = content
                content.update(trace_id=get_request_trace_id(request))

                response = MsgSpecJSONResponse(
                    status_code=status_code,
                    content=content,
                    background=background,
                )

                origin = request.headers.get('origin')
                if origin:
                    cors_middleware = CORSMiddleware(
                        app=app, # Pass the app to the middleware
                        allow_origins=settings.CORS_ALLOWED_ORIGINS,
                        allow_credentials=True,
                        allow_methods=['*'],
                        allow_headers=['*'],
                        expose_headers=settings.CORS_EXPOSE_HEADERS,
                    )
                    # Apply CORS headers manually
                    response.headers.update(cors_middleware.simple_headers)
                    has_cookie = 'cookie' in request.headers
                    
                    if cors_middleware.allow_all_origins and has_cookie:
                        response.headers['Access-Control-Allow-Origin'] = origin
                    elif not cors_middleware.allow_all_origins and cors_middleware.is_allowed_origin(origin=origin):
                        response.headers['Access-Control-Allow-Origin'] = origin
                        response.headers.add_vary_header('Origin')
                return response

# Instantiate the handler once at the module level
exception_handler: ExceptionHandler = ExceptionHandler()