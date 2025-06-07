
from fastapi import APIRouter, Request

from src.backend.device.schemas import DeviceAddRequest
from src.common.response.response_schema import ResponseSchemaModel, response_base
from src.common.security.jwt import DependsJwtAuth
from src.database.db import DBSession
from src.backend.device.service import device_service

router = APIRouter(prefix="/device", tags=["device"])

@router.post("/add", dependencies=[DependsJwtAuth])
async def add_device(db: DBSession, obj: DeviceAddRequest, request: Request) -> ResponseSchemaModel[None]:
    await device_service.add_device(request,db,obj)
    return response_base.success()