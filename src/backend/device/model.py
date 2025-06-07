
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.model import Base, id_key

if TYPE_CHECKING:
    from src.backend.user.model import User

class Device(Base):
    __tablename__ = "device"

    id: Mapped[id_key] = mapped_column(init=False)
    device_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment='Device Id')
    device_type: Mapped[int] = mapped_column(Integer,  comment='Device type')
    user: Mapped["User"] = relationship("User", back_populates="devices", init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True, comment='Reference to user')

    # optional
    notification_token: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment='Notification token')