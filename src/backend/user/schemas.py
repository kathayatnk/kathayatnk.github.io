from pydantic import Field, validate_email
from src.backend.card.schemas import CardGetRelationResponse
from src.common.data_classes import Token
from src.common.exception import errors
from src.common.schema import SchemaBase

class User(SchemaBase):
    id: int
    name: str | None
    email: str | None

class RegisterRequest(SchemaBase):
    name: str
    email: str
    password: str
    device_id: str = Field(description='Unique id to identify the current user device')

    def validate(self):
        if not self.password:
            raise errors.DataValidationError(msg='Password is required.')
        if not self.device_id:
            raise errors.DataValidationError(msg='Device id is required.')
        if not self.email:
            raise errors.DataValidationError(msg='Email is required.')
        try:
            validate_email(self.email)
        except Exception:
            raise errors.DataValidationError(msg='Email is invalid.')

class RegisterResponse(SchemaBase):
    token: Token
    user: User

class ProfileResponse(SchemaBase):
    id: int
    name: str | None
    email: str | None

class AssignCardRequest(SchemaBase):
    card_ids: list[int]

class AssignedCardResponse(CardGetRelationResponse):
    '''Get the Card detail with bank attached'''