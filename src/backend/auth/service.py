
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.auth.schemas import GuestLoginRequest, GuestLoginResponse, LoginRequest, LoginResponse, LogoutRequest, NewToken
from src.backend.user.model import User
from src.common.data_classes import RefreshToken
from src.common.security.password_secret import password_secret
from src.common.security.jwt import jwt_token
from src.backend.user.crud import user_dao
from src.backend.device.crud import device_dao
from src.common.exception import errors
from src.common.log import log
from src.core.settings import settings
from src.database.redis import redis

class AuthService:
    @staticmethod
    async def verify_user(db: AsyncSession, email: str, password: str | None) -> User:
        user = await user_dao.get_by_email(db, email)
        if not user:
            raise errors.NotFoundError(msg='Incorrect email or password')
        if user.password is None:
            raise errors.AuthorizationError(msg='Incorrect email or password')
        else:
            if not password_secret.password_verify(password, user.password):
                raise errors.AuthorizationError(msg='Incorrect email or password')
        if not user.status:
            raise errors.AuthorizationError(msg='Your account has been disabled. Please contact adminstrator')
        return user
    
    async def guest_login(self, *, db: AsyncSession, obj:GuestLoginRequest):
        try:

            # Check guest user and create if not present
            user = None
            user = await user_dao.get_by_guest_id(db, obj.device_id)
            if not user:
                await user_dao.create(db, {'guest_id': obj.device_id})
                await db.flush() 
                user = await user_dao.get_by_guest_id(db, obj.device_id)
                if not user:
                    raise errors.ServerError(msg='Unable to create user')
                
            await user_dao.update_login_time_guest(db, obj.device_id)
            await db.refresh(user)
            token = await jwt_token.create_token(user_id=str(user.id)) 
            data = GuestLoginResponse(token=token, user=user) 
            await db.commit()
            return data
        except Exception as e:
            log.error(e)
            raise e
            
    
    async def login(self, *, db: AsyncSession, obj:LoginRequest) -> LoginResponse:
        try:
            user = await self.verify_user(db, obj.email, obj.password)
            await user_dao.update_login_time(db, obj.email)
            await db.refresh(user)
            token = await jwt_token.create_token(user_id=str(user.id)) # TODO: make token with device id for multi device login
            data = LoginResponse(token=token, user=user) 
            await db.commit()
            return data
        except Exception as e:
            log.error(f'Login error: {e}')
            raise e
            

    async def create_new_token(self, *, db: AsyncSession, refresh_token: str) -> NewToken:
        if not refresh_token:
            raise errors.TokenError(msg='Refresh Token has expired, please log in again')
        try:
            token_info = jwt_token.jwt_decode(refresh_token)
            user_id = token_info.id
            user = await user_dao.get_by_id(db, user_id)
            if not user:
                raise errors.TokenError(msg='Refresh Token has expired, please log in again')
            elif not user.status:
                raise errors.AuthorizationError(msg='User has been locked, please contact the system administrator')
            refresh_token_obj = RefreshToken(refresh_token=refresh_token,refresh_token_expire_time=token_info.expire_time)
            token = await jwt_token.create_new_token(user.id, refresh_token_obj)
            newToken = NewToken(access_token=token.access_token, refresh_token=token.refresh_token)
            return newToken
        except Exception as e:
            raise e
            
    async def logout(self,db: AsyncSession,request: Request, obj: LogoutRequest) -> None:
        try:
            token_payload = await jwt_token.verify_auth_user(request)
            await device_dao.delete_by_device_id(db, obj.device_id)
            await redis.delete(f'{settings.TOKEN_REDIS_PREFIX}:{token_payload.id}:{token_payload.session_uuid}')
            await redis.delete(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{token_payload.id}:{obj.refresh_token}')
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        

auth_service: AuthService = AuthService()