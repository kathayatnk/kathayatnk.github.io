from typing import Any
from sqlalchemy import Select, inspect, or_, select
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.bank.model import Bank
from src.backend.card.model import Card

class CardCRUD(CRUDPlus[Card]):
    def _filter_input_dict(self, input_dict: dict[str, Any]) -> dict[str, Any]:
        mapper = inspect(self.model)
        valid_attrs = {attr.key for attr in mapper.attrs}
        return {k: v for k, v in input_dict.items() if k in valid_attrs}
    
    async def get_by_ids(self, db: AsyncSession, ids: list[int]) -> list[Card]:
        result = await self.select_models(db, self.model.id.in_(ids))
        return result
    
    async def create(self, db: AsyncSession, obj: dict[str, Any]):
        filtered_obj = self._filter_input_dict(obj)
        card = self.model(**filtered_obj)
        db.add(card)

    async def card_list_stmt(self, q: str) -> Select:
        stmt = select(self.model)
        stmt = stmt.options(selectinload(self.model.bank))
        if q:
            search_term = f"%{q.lower()}%"
            stmt = stmt.join(Card.bank).where(
                or_(
                    Card.name.ilike(search_term), 
                    Bank.name.ilike(search_term) 
                )
            )
        stmt = stmt.order_by(Card.name, Card.id)
        return stmt

card_dao: CardCRUD = CardCRUD(Card)