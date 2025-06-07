# src/backend/user/model.py
from datetime import datetime
from typing import TYPE_CHECKING
# from typing import TYPE_CHECKING # You can remove this import if you don't use it elsewhere for type hints
from sqlalchemy import VARBINARY, String, DateTime
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.model import Base, id_key
from src.utils.timezone import timezone

if TYPE_CHECKING:
    from src.backend.device.model import Device 
    from src.backend.card.model import Card

class User(Base):
    __tablename__ = 'user'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str | None] = mapped_column(String(100), unique=True, index=True,nullable=True, default=None, comment='Name of the User')
    guest_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True, default=None, comment='Guest Id')
    password: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment='Password')
    email: Mapped[str | None] = mapped_column(String(80), nullable=True, default=None, unique=True, index=True, comment='Email')
    status: Mapped[int] = mapped_column(default=1, index=True, comment='User account status')
    salt: Mapped[bytes | None] = mapped_column(VARBINARY(255).with_variant(BYTEA(255), 'postgresql'), nullable=True, default=None, comment='')
    last_login_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), init=False, onupdate=timezone.now, comment='Last login time')
    devices: Mapped[list["Device"]] = relationship("Device", back_populates="user", cascade="all, delete-orphan", default_factory=list)
    cards: Mapped[list["Card"]] = relationship("Card", secondary="user_cards", back_populates="users", default_factory=list)