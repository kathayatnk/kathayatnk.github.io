from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.device.schemas import DeviceAddRequest
from src.common.exception import errors
from src.backend.device.crud import device_dao 
from src.common.security.jwt import jwt_token
from src.backend.user.crud import user_dao

class DeviceService:
    async def add_device(self, request: Request, db: AsyncSession, obj: DeviceAddRequest):
        try:

            # Check auth status and get the user with relation to device 
            token_payload = await jwt_token.verify_auth_user(request)
            user = await user_dao.get_by_id_device_relation(db, token_payload.id)
            if not user:
                raise errors.ServerError(msg='Unable to add device')
            
             # check if device exists in the user devices list
            existing_assignment = next((d for d in user.devices if d.device_id == obj.device_id),None)

            # create or update device
            device = await device_dao.get_by_device_id(db, obj.device_id)
            if not device:
                dict_obj = obj.model_dump()
                dict_obj['user_id'] = token_payload.id
                await device_dao.create(db, dict_obj)
                await db.flush()
            else:
               await device_dao.update(db, device.id, obj.model_dump())
            
            # If the device is not in the user devices list, add it
            if not existing_assignment:
                device = await device_dao.get_by_device_id(db, obj.device_id)
                user.devices.append(device)
            
            # commit the transaction
            await db.commit()

        except Exception as e:
            await db.rollback()
            raise e
        
            

device_service: DeviceService = DeviceService()