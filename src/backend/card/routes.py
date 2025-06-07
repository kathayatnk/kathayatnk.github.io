from fastapi import APIRouter, Query

from src.backend.card.schemas import CardAddRequest, CardGetRelationResponse, CardGetResponse
from src.common.pagination import DependsPagination, PageData
from src.common.response.response_schema import ResponseSchemaModel, response_base
from src.database.db import DBSession
from src.backend.card.service import card_service


router = APIRouter(prefix="/card", tags=["card"])

@router.post("/add")
async def add_card(db:DBSession, obj: CardAddRequest) -> ResponseSchemaModel[CardGetResponse]:
    return

@router.get("/list", dependencies=[DependsPagination])
async def list_cards(db: DBSession) -> ResponseSchemaModel[PageData[CardGetRelationResponse]]:
    data = await card_service.card_list(db, '')
    return response_base.success(data=data)

@router.get("/search", dependencies=[DependsPagination])
async def search_cards(db: DBSession, q: str  = Query(description='search by bank or card names'),) -> ResponseSchemaModel[PageData[CardGetRelationResponse]]:
    data = await card_service.card_list(db,q)
    return response_base.success(data=data)