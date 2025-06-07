from fastapi import APIRouter, Request
from src.backend.auth.schemas import LoginRequest, LoginResponse, GuestLoginRequest, GuestLoginResponse, LogoutRequest, NewToken, RefreshTokenRequest
from src.common.response.response_schema import ResponseSchemaModel, response_base
from src.common.security.jwt import DependsJwtAuth
from src.database.db import DBSession
from src.backend.auth.service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/guest_login")
async def guest_login(db: DBSession, obj:GuestLoginRequest) -> ResponseSchemaModel[GuestLoginResponse]:
    data = await auth_service.guest_login(db=db, obj=obj)
    return response_base.success(data=data)

@router.post("/login")
async def login(db: DBSession, obj:LoginRequest) -> ResponseSchemaModel[LoginResponse]:
    data = await auth_service.login(db=db, obj=obj)
    return response_base.success(data=data)

@router.post("/refresh_token")
async def refresh_token(db: DBSession, obj: RefreshTokenRequest) -> ResponseSchemaModel[NewToken]:
    data = await auth_service.create_new_token(db=db, refresh_token=obj.refresh_token)
    return response_base.success(data=data)

@router.post("/logout", dependencies=[DependsJwtAuth])
async def logout(db: DBSession,request: Request, obj: LogoutRequest) -> ResponseSchemaModel[None]:
    await auth_service.logout(db, request, obj)
    return response_base.success()