from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from src.utils.timezone import timezone

id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='')
]

class UserMixin(MappedAsDataclass):
    created_by: Mapped[int] = mapped_column(sort_order=998, comment='')
    updated_by: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='')


class DateTimeMixin(MappedAsDataclass):
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=timezone.now, sort_order=999, comment=''
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, onupdate=timezone.now, sort_order=999, comment=''
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @declared_attr.directive
    def __table_args__(cls) -> dict:
        return {'comment': cls.__doc__ or ''}


class DataClassBase(MappedAsDataclass, MappedBase):
    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    __abstract__ = True
