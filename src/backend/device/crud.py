from typing import Any
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus
from src.backend.device.model import Device

class DeviceCRUD(CRUDPlus[Device]):
    def _filter_input_dict(self, input_dict: dict[str, Any]) -> dict[str, Any]:
        mapper = inspect(self.model)
        valid_attrs = {attr.key for attr in mapper.attrs}
        return {k: v for k, v in input_dict.items() if k in valid_attrs}

    async def get_by_device_id(self, db: AsyncSession, device_id: str) -> Device:
        return await self.select_model_by_column(db, device_id=device_id)
    
    async def create(self, db: AsyncSession, obj: dict[str, Any]):
        filtered_obj = self._filter_input_dict(obj)
        device = self.model(**filtered_obj)
        db.add(device)

    async def delete_by_device_id(self, db: AsyncSession, device_id: str) -> int:
        affected_row = await self.delete_model_by_column(db, device_id=device_id)
        return affected_row

    async def update(self,db: AsyncSession, device: int, obj: dict[str, Any]):
        filtered_obj = self._filter_input_dict(obj)
        await self.update_model(db, device, filtered_obj)

device_dao: DeviceCRUD = DeviceCRUD(Device)