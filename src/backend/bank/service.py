from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.bank.schemas import BankAddRequest, BankGetRelationResponse, BankGetResponse
from src.backend.bank.crud import bank_dao
from src.common.pagination import PageData, paging_data

class BankService:
    async def add_bank(self, db: AsyncSession, obj: BankAddRequest) -> BankGetResponse:
        try:
            dict_obj = obj.model_dump()
            await bank_dao.create(db, dict_obj)
            await db.flush()
            new_bank = await bank_dao.get_by_name(db, obj.name)
            return BankGetResponse.model_validate(new_bank)
        except Exception as e:
            raise e
        
    async def bank_list(self, db: AsyncSession, q: str) -> PageData[BankGetRelationResponse]:
        stmt = await bank_dao.bank_list_stmt(q)
        try:
            paged_data = await paging_data(db, stmt)
            return paged_data
        except Exception as e:
            raise e

bank_service: BankService = BankService()