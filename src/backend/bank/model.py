

from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.model import Base
from src.common.model import id_key

if TYPE_CHECKING:
    from src.backend.card.model import Card


class Bank(Base):
    __tablename__ = "bank"

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment='Bank name')
    logo_url: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment='URL to bank logo')
    website: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, comment='Bank website URL')
    status: Mapped[int] = mapped_column(default=1, index=True, comment='Bank status (active/inactive)')
    cards: Mapped[list["Card"]] = relationship("Card",back_populates='bank',cascade='all, delete-orphan',default_factory=list)

    def __repr__(self) -> str:
        return f"<Bank(id={self.id}, name='{self.name}')>"