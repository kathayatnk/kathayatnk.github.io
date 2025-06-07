from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination

from src.common.exception.exception_handler import exception_handler
from src.common.health_check import http_limit_callback
from src.middleware.middleware import middleware
from src.utils.serializers import MsgSpecJSONResponse
from src.database.redis import redis
from src.core.settings import settings
from src.database.db import db
from src.common.log import log
from src.backend.routes import router 
from src.backend.root.root import router as root_router 


class Registrar:

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:

        # Open database connection 
        await db.open()

        # Open the redis connection
        await redis.open()

        # Set the rate limiter
        await FastAPILimiter.init(redis=redis,prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,http_callback=http_limit_callback)

        yield

        # Close redis connection
        await redis.close()

        # Close rate limiter
        await FastAPILimiter.close()

    def register(self) -> FastAPI:
        app = FastAPI(lifespan=self.lifespan, 
                      default_response_class=MsgSpecJSONResponse,
                      title=settings.FASTAPI_TITLE,
                      version=settings.FASTAPI_VERSION,
                      description=settings.FASTAPI_DESCRIPTION,
                      docs_url=settings.FASTAPI_DOCS_URL,
                      redoc_url=settings.FASTAPI_REDOC_URL,
                      openapi_url=settings.FASTAPI_OPENAPI_URL)

        # Register middleware
        middleware.register(app)

        # Register routes
        app.include_router(root_router)
        app.include_router(router)

        # Register logging
        log.register()

        # Register exception handler
        exception_handler.register(app)

        # Add the pagination
        add_pagination(app)

        # Return the app
        return app

registrar: Registrar = Registrar()