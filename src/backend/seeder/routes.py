
from fastapi import APIRouter

from src.backend.seeder.seeder import seeder
from src.common.response.response_schema import ResponseSchemaModel, response_base
from src.database.db import DBSession

router = APIRouter(prefix="/seeder", tags=["seed"])


@router.post('/seed_initial_data')
async def seed_initial_data(db: DBSession) -> ResponseSchemaModel[None]:
    await seeder.seed_initial_data(db)
    return response_base.success()