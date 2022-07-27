from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


engine = create_async_engine(
                        getattr(settings, 'pg_dsn'),
                        echo=getattr(settings, 'pg_echo'),
                        future=getattr(settings, 'pg_future')
                    )


async def init_db(engine=engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    await engine.dispose()


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session