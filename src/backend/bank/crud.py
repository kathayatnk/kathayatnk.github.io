from typing import Any
from sqlalchemy import Select, inspect,select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from src.backend.bank.model import Bank
from src.backend.card.model import Card

class BankCRUD(CRUDPlus[Bank]):
    def _filter_input_dict(self, input_dict: dict[str, Any]) -> dict[str, Any]:
        mapper = inspect(self.model)
        valid_attrs = {attr.key for attr in mapper.attrs}
        return {k: v for k, v in input_dict.items() if k in valid_attrs}
     
    async def create(self, db: AsyncSession, obj: dict[str, Any]):
        filtered_obj = self._filter_input_dict(obj)
        bank = self.model(**filtered_obj)
        db.add(bank)
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Bank:
        return await self.select_model_by_column(db, name=name)
    
    async def get_all(self, db: AsyncSession) -> list[Bank]:
        stmt = (select(self.model))
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def bank_list_stmt(self, q: str) -> Select:
        stmt = select(self.model)
        stmt = stmt.options(selectinload(self.model.cards))
        if q:
            search_term = f"%{q.lower()}%"
            stmt = stmt.join(Bank.cards).where(
                or_(
                    Card.name.ilike(search_term), 
                    Bank.name.ilike(search_term) 
                )
            )
        stmt = stmt.order_by(Bank.name,Bank.id)
        return stmt

bank_dao: BankCRUD = BankCRUD(Bank)