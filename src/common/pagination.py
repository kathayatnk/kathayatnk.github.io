#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING, Any, Generic, Sequence, TypeVar

from fastapi import Depends, Query
from fastapi_pagination import pagination_ctx
from fastapi_pagination.bases import AbstractPage, AbstractParams, RawParams
from fastapi_pagination.ext.sqlalchemy import apaginate
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T')
SchemaT = TypeVar('SchemaT')


class _CustomPageParams(BaseModel, AbstractParams):
    """Custom pagination parameters"""

    page: int = Query(1, ge=1, description='Page number')
    size: int = Query(20, gt=0, le=200, description='Number of items per page')

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.size,
            offset=self.size * (self.page - 1),
        )


class _Links(BaseModel):
    """Pagination links"""

    first: str = Field(description='Link to the first page')
    last: str = Field(description='Link to the last page')
    self: str = Field(description='Link to the current page')
    next: str | None = Field(None, description='Link to the next page')
    prev: str | None = Field(None, description='Link to the previous page')


class _PageDetails(BaseModel):
    """Pagination details"""

    items: list = Field([], description='List of items on the current page')
    total: int = Field(description='Total number of items')
    page: int = Field(description='Current page number')
    size: int = Field(description='Number of items per page')
    total_pages: int = Field(description='Total number of pages')


class _CustomPage(_PageDetails, AbstractPage[T], Generic[T]):
    """Custom pagination class"""

    __params_type__ = _CustomPageParams

    @classmethod
    def create(
        cls,
        items: list,
        params: _CustomPageParams,
        total: int = 0,
    ) -> _CustomPage[T]:
        page = params.page
        size = params.size
        total_pages = ceil(total / size)
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages,
        )


class PageData(_PageDetails, Generic[SchemaT]):
    """
    Standard response model for pagination APIs that includes the data schema

    Example::

        @router.get('/test', response_model=ResponseSchemaModel[PageData[GetApiDetail]])
        def test():
            return ResponseSchemaModel[PageData[GetApiDetail]](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[PageData[GetApiDetail]]:
            return ResponseSchemaModel[PageData[GetApiDetail]](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[PageData[GetApiDetail]]:
            res = CustomResponseCode.HTTP_200
            return ResponseSchemaModel[PageData[GetApiDetail]](code=res.code, msg=res.msg, data=GetApiDetail(...))
    """

    items: Sequence[SchemaT]


async def paging_data(db: AsyncSession, select: Select) -> dict[str, Any]:
    """
    Create pagination data using SQLAlchemy

    :param db: Database session
    :param select: SQL query statement
    :return:
    """
    paginated_data: _CustomPage = await apaginate(db, select)
    return paginated_data


# Pagination dependency injection
DependsPagination = Depends(pagination_ctx(_CustomPage))

