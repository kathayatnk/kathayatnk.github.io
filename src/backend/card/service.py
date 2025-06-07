
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.card.schemas import CardGetRelationResponse
from src.common.pagination import PageData, paging_data
from src.backend.card.crud import card_dao


class CardService:

    async def card_list(self, db: AsyncSession, q: str) -> PageData[CardGetRelationResponse]:
        stmt = await card_dao.card_list_stmt(q)
        try:
            paged_data = await paging_data(db, stmt)
            return paged_data
        except Exception as e:
            raise e
        
card_service: CardService = CardService()