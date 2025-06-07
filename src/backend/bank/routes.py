
from fastapi import APIRouter, Query

from src.backend.bank.schemas import BankAddRequest,BankGetResponse,BankGetRelationResponse
from src.common.response.response_schema import ResponseSchemaModel, response_base
from src.database.db import DBSession
from src.backend.bank.service import bank_service
from src.common.pagination import DependsPagination, PageData

router = APIRouter(prefix="/bank", tags=["bank"])

@router.post("/add")
async def add_bank(db:DBSession, obj: BankAddRequest) -> ResponseSchemaModel[BankGetResponse]:
    data = await bank_service.add_bank(db, obj)
    return response_base.success(data=data)

@router.get("/list", dependencies=[DependsPagination])
async def list_banks(db: DBSession) -> ResponseSchemaModel[PageData[BankGetRelationResponse]]:
    data = await bank_service.bank_list(db,'')
    return response_base.success(data=data)

@router.get("/search", dependencies=[DependsPagination])
async def search_bank(db: DBSession, q: str  = Query(description='search by bank or card names'),) -> ResponseSchemaModel[PageData[BankGetRelationResponse]]:
    data = await bank_service.bank_list(db,q)
    return response_base.success(data=data)