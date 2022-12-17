"""
directly insert after creating database
"""


from time import perf_counter

from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.db import init_data


async def init_db() -> None:
    connectable = create_async_engine(str(settings.db_url))

    async with connectable.connect() as connection:
        session = AsyncSession(bind=connection)

    await connectable.dispose()
