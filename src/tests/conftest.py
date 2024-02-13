import pytest
import asyncio
from db import engine, Base


@pytest.fixture(scope="session", autouse=True)
def create_model():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_create_model())


async def _create_model():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
