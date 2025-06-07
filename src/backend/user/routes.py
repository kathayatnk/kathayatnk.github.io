
from fastapi import APIRouter, Request

from src.backend.user.schemas import AssignCardRequest, AssignedCardResponse, ProfileResponse, RegisterRequest, RegisterResponse
from src.common.response.response_schema import ResponseSchemaModel, response_base
from src.common.security.jwt import DependsJwtAuth
from src.database.db import DBSession
from src.backend.user.service import user_service

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register(db: DBSession, obj: RegisterRequest) -> ResponseSchemaModel[RegisterResponse]:
    data = await user_service.register(db, obj)
    return response_base.success(data=data)

@router.post("/forgot_password")
async def forgot_password():
    return

@router.post("/cards", dependencies=[DependsJwtAuth], description='assign selected cards to user')
async def set_cards(db: DBSession, request: Request, obj: AssignCardRequest) -> ResponseSchemaModel[None]:
    await user_service.assign_cards(db, request, obj)
    return response_base.success()

@router.get("/me", dependencies=[DependsJwtAuth])
async def me(db: DBSession, request: Request) -> ResponseSchemaModel[ProfileResponse]:
    data = await user_service.get_profile(db, request)
    return response_base.success(data=data)

@router.get("/cards", dependencies=[DependsJwtAuth])
async def user_cards(db: DBSession, request: Request) -> ResponseSchemaModel[list[AssignedCardResponse]]:
    data = await user_service.get_user_cards(db, request)
    return response_base.success(data=data)