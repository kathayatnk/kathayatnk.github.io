from datetime import datetime
from pydantic import  Field
from src.backend.user.schemas import User
from src.common.schema import SchemaBase

class AccessToken(SchemaBase):
    access_token: str
    access_token_expire_time: datetime

class RefreshToken(SchemaBase):
    refresh_token: str
    refresh_token_expire_time: datetime

class RefreshTokenRequest(SchemaBase):
    refresh_token: str

class NewToken(SchemaBase):
    access_token: AccessToken
    refresh_token: RefreshToken

class LoginRequest(SchemaBase):
    email: str
    password: str

class GuestLoginRequest(SchemaBase):
    device_id: str = Field(description='Unique id to identify the current user device')

class GuestLoginResponse(SchemaBase):
    token: NewToken
    user: User

class LoginResponse(SchemaBase):
    token: NewToken
    user: User

class LogoutRequest(SchemaBase):
    refresh_token: str
    device_id: str