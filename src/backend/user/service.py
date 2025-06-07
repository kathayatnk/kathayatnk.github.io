import bcrypt
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.user.crud import user_dao
from src.backend.user.schemas import AssignCardRequest, AssignedCardResponse, ProfileResponse, RegisterRequest, RegisterResponse
from src.common.exception import errors
from src.common.security.password_secret import password_secret
from src.common.security.jwt import jwt_token
from src.backend.card.crud import card_dao

class UserService:
    async def register(self, db: AsyncSession, obj: RegisterRequest) -> RegisterResponse:
     try:
        
         # validate the object 
         obj.validate()

         # check if user already exsists 
         actual_user = await user_dao.get_by_email(db, obj.email)
         if actual_user:
           raise errors.ForbiddenError(msg='User already exists')

         # check if we have guest user
         guest_user = await user_dao.get_by_guest_id(db, obj.device_id)
         if guest_user:
           salt = bcrypt.gensalt()
           obj.password = password_secret.get_hash_password(obj.password, salt)
           dict_obj = obj.model_dump()
           dict_obj.update({'salt': salt})
           dict_obj.update({'guest_id': None})
           await user_dao.update(db, guest_user.id, dict_obj)
         else:
           salt = bcrypt.gensalt()
           obj.password = password_secret.get_hash_password(obj.password, salt)
           dict_obj = obj.model_dump()
           dict_obj.update({'salt': salt})
           await user_dao.create(db, dict_obj)

         await db.flush()
         new_user = await user_dao.get_by_email(db, obj.email)
         if not new_user:
           raise errors.ServerError(msg='Unable to register at the moment')

         await user_dao.update_login_time(db, obj.email)
         await db.refresh(new_user)
         token = await jwt_token.create_token(user_id=str(new_user.id)) 
         data = RegisterResponse(token=token, user=new_user) 
         await db.commit()
         return data
     except Exception as e:
       await db.rollback()
       raise e
    
    async def get_profile(self, db: AsyncSession, request: Request) -> ProfileResponse:
       try:
          token_payload = await jwt_token.verify_auth_user(request)
          user = await user_dao.get_by_id(db, token_payload.id)
          data = ProfileResponse.model_validate(user)
          return data
       except Exception as e:
          raise e
       
    async def assign_cards(self, db: AsyncSession, request: Request, obj: AssignCardRequest) -> None:
        try:
          token_payload = await jwt_token.verify_auth_user(request)
          user = await user_dao.get_by_id_card_relation(db,token_payload.id)
          if not user:
            raise errors.TokenError(msg='Not Authenticated')
          if not obj.card_ids:
            raise errors.NotFoundError(msg='Cards not provided. Please select at least one card')
          current_card_ids = {card.id for card in user.cards}
          unique_card_ids = list(set(obj.card_ids))
          found_cards = await card_dao.get_by_ids(db, unique_card_ids)
          if not found_cards:
              raise errors.NotFoundError(msg='No valid cards found for the provided IDs.')
          for card in found_cards:
              if card.id not in current_card_ids:
                  user.cards.append(card)
          await db.commit()
        except Exception as e:
          await db.rollback()
          raise e
    
    async def get_user_cards(self, db: AsyncSession, request: Request) -> list[AssignedCardResponse]:
        try:
          token_payload = await jwt_token.verify_auth_user(request)
          user = await user_dao.get_by_id_card_bank_relation(db, token_payload.id)
          if not user:
             raise errors.TokenError(msg='Not Authenticated')
          data = [AssignedCardResponse.model_validate(card) for card in user.cards]
          return data
        except Exception as e:
          raise e

user_service: UserService = UserService()