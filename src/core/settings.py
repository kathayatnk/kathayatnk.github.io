from typing import Literal
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.path_config import path_config


class Settings(BaseSettings):

    # Model
    model_config = SettingsConfigDict(env_file=f"{path_config.base_path}.env",env_file_encoding="utf-8",case_sensitive=True,extra='ignore')

    # Environment
    ENVIRONMENT: Literal["dev", "prod"]

    # Database 
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_ECHO: bool = False
    DATABASE_POOL_ECHO: bool = False

    # Redis
    REDIS_URL: str
    REDIS_TIMEOUT: int = 5

    # Rate limiter
    REQUEST_LIMITER_REDIS_PREFIX: str = 'swipewise:limiter'

    # DateTime Settings
    DATETIME_TIMEZONE: str = 'Asia/Kathmandu'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Logging
    LOG_CID_DEFAULT_VALUE: str = '-'
    LOG_CID_UUID_LENGTH: int = 32
    LOG_STD_LEVEL: str = 'DEBUG'
    LOG_ACCESS_FILE_LEVEL: str = 'DEBUG'
    LOG_ERROR_FILE_LEVEL: str = 'ERROR'
    LOG_STD_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOG_FILE_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOG_ACCESS_FILENAME: str = 'swipe_access.log'
    LOG_ERROR_FILENAME: str = 'swipe_error.log'

    # Trace ID
    TRACE_ID_REQUEST_HEADER_KEY: str = 'X-Request-ID'

    # Middleware Settings
    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_ACCESS: bool = True

    # FastAPI Settings
    FASTAPI_API_V1_PATH: str = '/api/v1'
    FASTAPI_TITLE: str = 'Swipewise API'
    FASTAPI_VERSION: str = '0.0.1'
    FASTAPI_DESCRIPTION: str = 'Swipewise API'
    FASTAPI_DOCS_URL: str = '/docs'
    FASTAPI_REDOC_URL: str = '/redoc'
    FASTAPI_OPENAPI_URL: str | None = '/openapi-swipewise'
    FASTAPI_STATIC_FILES: bool = True

    # Token Settings
    TOKEN_SECRET_KEY: str 
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24  # 1 day
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days
    TOKEN_REDIS_PREFIX: str = 'swipewise:token'
    TOKEN_EXTRA_INFO_REDIS_PREFIX: str = 'swipewise:token_extra_info'
    TOKEN_ONLINE_REDIS_PREFIX: str = 'swipewise:token_online'
    TOKEN_REFRESH_REDIS_PREFIX: str = 'swipewise:refresh_token'

    # Exclude path from authrorization
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [
        f'{FASTAPI_API_V1_PATH}/auth/login', 
        f'{FASTAPI_API_V1_PATH}/auth/guest_login', 
        f'{FASTAPI_API_V1_PATH}/auth/register',
        f'{FASTAPI_API_V1_PATH}/auth/forgot_password',
        f'{FASTAPI_API_V1_PATH}/card/search'
    ]

    # IP Location Settings
    IP_LOCATION_PARSE: Literal['online', 'offline', 'false'] = 'offline'
    IP_LOCATION_REDIS_PREFIX: str = 'swipewise:ip:location'
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24  

    # CORS Settings
    CORS_ALLOWED_ORIGINS: list[str] = [
        'http://127.0.0.1:8000',
        'http://localhost:5173',
    ]
    CORS_EXPOSE_HEADERS: list[str] = [
        'X-Request-ID',
    ]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings: Settings = get_settings()