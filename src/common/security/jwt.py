# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
from datetime import timedelta
import json
from typing import Any
from uuid import uuid4

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt

from src.common.data_classes import AccessToken, Token, RefreshToken, TokenPayload
from src.common.exception.errors import TokenError
from src.core.settings import settings
from src.database.redis import redis
from src.utils.timezone import timezone

# JWT authorization dependency injection
DependsJwtAuth = Depends(HTTPBearer())

class JWTToken:

    def _jwt_encode(self,payload: dict[str, Any]) -> str:
        return jwt.encode(
            payload,
            settings.TOKEN_SECRET_KEY,
            settings.TOKEN_ALGORITHM,
        )

    def jwt_decode(self,token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
            session_uuid = payload.get('session_uuid') or 'debug'
            user_id = payload.get('sub')
            expire_time = payload.get('exp')
            if not user_id:
                raise TokenError(msg='Invalid token')
        except ExpiredSignatureError:
            raise TokenError(msg='Token has expired')
        except (JWTError, Exception):
            raise TokenError(msg='Invalid token')
        return TokenPayload(id=int(user_id), session_uuid=session_uuid, expire_time=expire_time)
    
    async def jwt_authentication(self,token: str) -> TokenPayload:
        token_payload = self.jwt_decode(token)
        user_id = token_payload.id
        redis_token = await redis.get(f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token_payload.session_uuid}')
        if not redis_token:
            raise TokenError(msg='Token expired')

        if token != redis_token:
            raise TokenError(msg='Token invalid')
        
        return token_payload

    async def create_token(self, user_id: str, **kwargs) -> Token:
        accessToken = await self._create_access_token(user_id, **kwargs)
        refreshToken =  await self._create_refresh_token(user_id)
        return Token(access_token=accessToken, refresh_token=refreshToken)

    async def _create_access_token(self, user_id: str, **kwargs) -> AccessToken:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        session_uuid = str(uuid4())
        access_token = self._jwt_encode({
            'session_uuid': session_uuid,
            'exp': expire,
            'sub': user_id,
        })

        await redis.setex(
            f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}',
            settings.TOKEN_EXPIRE_SECONDS,
            access_token,
        )

        # Store additional token information separately if needed
        if kwargs:
            await redis.setex(
                f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{session_uuid}',
                settings.TOKEN_EXPIRE_SECONDS,
                json.dumps(kwargs, ensure_ascii=False),
            )
        return AccessToken(access_token=access_token, access_token_expire_time=expire, session_uuid=session_uuid)

    async def _create_refresh_token(self, user_id: str) -> RefreshToken:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
        refresh_token = self._jwt_encode({'exp': expire, 'sub': user_id})
        await redis.setex(
            f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{refresh_token}',
            settings.TOKEN_REFRESH_EXPIRE_SECONDS,
            refresh_token,
        )
        return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)
    

    async def create_new_token(self,user_id: str, token: RefreshToken, **kwargs) -> Token:
        redis_refresh_token = await redis.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{token.refresh_token}')
        if not redis_refresh_token or redis_refresh_token != token.refresh_token:
            raise TokenError(msg='Refresh token has expired, please log in again')
        access_token = await self._create_access_token(user_id, **kwargs)
        return Token(access_token=access_token, refresh_token=token)
    
    def get_token(self,request: Request) -> str:
        authorization = request.headers.get('Authorization')
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            raise TokenError(msg='Invalid token')
        return token

    async def revoke_token(self,user_id: str, session_uuid: str) -> None:
        token_key = f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}'
        await redis.delete(token_key)

    async def verify_auth_user(self,request: Request) -> TokenPayload | None:
        token = self.get_token(request)
        token_payload = self.jwt_decode(token)
        return token_payload

jwt_token: JWTToken = JWTToken()