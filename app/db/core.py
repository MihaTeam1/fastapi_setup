from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import database as db_conf

db_url = (
        f'{db_conf.db_driver}://'
        f'{db_conf.db_user}:'
        f'{db_conf.db_pass}@'
        f'{db_conf.db_host}:'
        f'{db_conf.db_port}/'
        f'{db_conf.db_name}'
    )
engine = create_async_engine(
                        db_url,
                        echo=db_conf.echo,
                        future=db_conf.future
                    )

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session