from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from src.core.settings import settings
from src.middleware.jwt_auth_middleware import JwtAuthMiddleware
from src.middleware.state_middleware import StateMiddleware



class Middleware:
    def register(self, app: FastAPI) -> None:
        
        app.add_middleware(AuthenticationMiddleware,
                           backend=JwtAuthMiddleware(),
                           on_error=JwtAuthMiddleware.auth_exception_handler)
        
        app.add_middleware(StateMiddleware)

        app.add_middleware(CorrelationIdMiddleware, validator=False)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )

middleware: Middleware = Middleware()