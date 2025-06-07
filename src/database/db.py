import sys
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.common.model import MappedBase
from src.core.settings import settings
from src.common.log import log

class Postgress:
    def __init__(self) -> None:
        self.engine = None
        self.db_session = None
        self.url = URL.create(drivername='postgresql+asyncpg', 
                              username=settings.DATABASE_USER, 
                              password=settings.DATABASE_PASSWORD, 
                              host=settings.DATABASE_HOST, 
                              port=settings.DATABASE_PORT, 
                              database=settings.DATABASE_NAME)
    
    async def open(self) -> None:
        try:
            self.engine = create_async_engine(self.url,
                                              echo=settings.DATABASE_ECHO,
                                              echo_pool=settings.DATABASE_POOL_ECHO,
                                              future=True,
                                              pool_size=10,  
                                              max_overflow=20, 
                                              pool_timeout=30, 
                                              pool_recycle=3600,  
                                              pool_pre_ping=True,  
                                              pool_use_lifo=False)
        except Exception as e:
            log.error('❌ Database connection failed {}', e)
            sys.exit()
        else:
            self.db_session = async_sessionmaker(bind=self.engine,
                                                 class_=AsyncSession,
                                                 autoflush=False,  
                                                 expire_on_commit=False)
    
    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()
            log.info("✅ Database connection closed")

    async def create_table(self) -> None:
        if self.engine:
            async with self.engine.begin() as coon:
                await coon.run_sync(MappedBase.metadata.create_all)
        
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.db_session() as session:
            yield session


db: Postgress = Postgress()
DBSession = Annotated[AsyncSession, Depends(db.get_db)]

