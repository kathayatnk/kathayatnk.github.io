import dataclasses
from datetime import datetime


@dataclasses.dataclass
class IpInfo:
    ip: str
    country: str | None
    region: str | None
    city: str | None


@dataclasses.dataclass
class UserAgentInfo:
    user_agent: str
    os: str | None
    browser: str | None
    device: str | None


@dataclasses.dataclass
class AccessToken:
    access_token: str
    access_token_expire_time: datetime
    session_uuid: str


@dataclasses.dataclass
class RefreshToken:
    refresh_token: str
    refresh_token_expire_time: datetime

@dataclasses.dataclass
class Token:
    access_token: AccessToken
    refresh_token: RefreshToken


@dataclasses.dataclass
class TokenPayload:
    id: int
    session_uuid: str
    expire_time: datetime

