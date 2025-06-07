
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import INTEGER
from src.common.model import Base, id_key
from src.backend.m2m import user_cards

if TYPE_CHECKING:
    from src.backend.bank.model import Bank
    from src.backend.user.model import User



class Card(Base):
    __tablename__ = "card"

    id: Mapped[id_key] = mapped_column(init=False)
    bank_id: Mapped[int] = mapped_column(ForeignKey('bank.id'), index=True, comment='Reference to bank')
    name: Mapped[str] = mapped_column(String(100), index=True, comment='Card name')
    bank: Mapped["Bank"] = relationship("Bank", back_populates='cards', init=False)
    users: Mapped[list["User"]] = relationship("User",secondary=user_cards, back_populates="cards",default_factory=list)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment='Card description')
    annual_fee: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None, comment='Annual fee in cents')
    reward_desc: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None, comment='Description of rewards')
    interest_rate: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None, comment='APR in basis points')
    min_credit_score: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None, comment='Minimum recommended credit score')
    status: Mapped[int] = mapped_column(default=1, index=True, comment='Card status (active/inactive)')
    is_featured: Mapped[bool] = mapped_column(Boolean().with_variant(INTEGER, 'postgresql'), default=False, comment='Featured card flag')