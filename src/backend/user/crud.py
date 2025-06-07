from typing import Any
from sqlalchemy import inspect, select
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.card.model import Card
from src.backend.user.model import User
from src.utils.timezone import timezone

class UserCRUD(CRUDPlus[User]):

    def _filter_input_dict(self, input_dict: dict[str, Any]) -> dict[str, Any]:
        mapper = inspect(self.model)
        valid_attrs = {attr.key for attr in mapper.attrs}
        return {k: v for k, v in input_dict.items() if k in valid_attrs}
    
    async def get_by_email(self, db: AsyncSession, email: str) -> User:
       user = await self.select_model_by_column(db, email=email)
       return user
    
    async def get_by_id(self, db: AsyncSession, user_id: int) -> User:
        user = await self.select_model(db,user_id)
        return user
    
    async def get_by_guest_id(self, db: AsyncSession, guest_id: str) -> User:
        user = await self.select_model_by_column(db, guest_id=guest_id)
        return user
    
    async def create(self, db: AsyncSession, obj: dict[str, Any]):
        filter_obj = self._filter_input_dict(obj)
        user = self.model(**filter_obj)
        db.add(user)

    async def update_login_time_guest(self, db: AsyncSession, guest_id: str) -> int:
        return await self.update_model_by_column(db, {'last_login_time': timezone.now()}, guest_id=guest_id)
    
    async def update_login_time(self, db: AsyncSession, email: str) -> int:
        return await self.update_model_by_column(db, {'last_login_time': timezone.now()}, email=email)
    
    async def get_by_id_device_relation(self, db: AsyncSession, user_id: int) -> User | None:
        stmt = (
        select(self.model)
            .options(selectinload(User.devices))  
            .where(self.model.id == user_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first() 
    
    async def get_by_id_card_relation(self, db: AsyncSession, id: int) -> User | None:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.cards) 
            )
            .where(self.model.id == id)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user
    
    async def get_by_id_card_bank_relation(self, db: AsyncSession, id: int) -> User | None:
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.cards).selectinload(Card.bank) 
            )
            .where(self.model.id == id)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        return user
    
    async def update(self,db: AsyncSession, user: User, obj: dict[str, Any]):
        filter_obj = self._filter_input_dict(obj)
        await self.update_model(db, user, filter_obj)
    
user_dao: UserCRUD = UserCRUD(User)