from typing import Any
from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError
from starlette.requests import HTTPConnection

from src.common.data_classes import TokenPayload
from src.common.log import log
from src.common.exception.errors import TokenError
from src.common.security.jwt import jwt_token
from src.core.settings import settings
from src.utils.serializers import MsgSpecJSONResponse


class _AuthenticationError(AuthenticationError):
    """Override internal authentication error class"""

    def __init__(
        self, *, code: int | None = None, msg: str | None = None, headers: dict[str, Any] | None = None
    ) -> None:
        """
        Initialize authentication error

        :param code: Error code
        :param msg: Error message
        :param headers: Response headers
        :return:
        """
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT authentication middleware"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: _AuthenticationError) -> Response:
        """
        Override internal authentication error handling

        :param conn: HTTP connection object
        :param exc: Authentication error object
        :return:
        """
        return MsgSpecJSONResponse(content={'code': exc.code, 'msg': exc.msg, 'data': None}, status_code=exc.code)

    async def authenticate(self, request: Request) -> tuple[AuthCredentials, TokenPayload] | None:
        """
        Authenticate request

        :param request: FastAPI request object
        :return:
        """
        token = request.headers.get('Authorization')
        if not token:
            return None

        if request.url.path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return None

        scheme, token = get_authorization_scheme_param(token)
        if scheme.lower() != 'bearer':
            return None

        try:
            payload = await jwt_token.jwt_authentication(token)
        except TokenError as exc:
            raise _AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception as e:
            log.exception(f'JWT authorization exception: {e}')
            raise _AuthenticationError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        return AuthCredentials(['authenticated']), payload