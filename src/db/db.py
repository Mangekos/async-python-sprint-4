# import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

# from src.core.config import app_settings, db_echo_mode
from models.base import Base
from models.crossings import Crossings
from models.links import Links

engine = create_async_engine(
    # database_dsn,
    "sqlite+aiosqlite:///fastapi.db",
    echo=True,
    future=True,
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_model() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def ping() -> bool:
    async with async_session() as session:
        try:
            await session.get(Links, 1)
            return True
        except OperationalError:
            return False


async def get_all_links() -> list[Links]:
    async with async_session() as session:
        query: Links = select(Links)
        links = (await session.scalars(query)).all()
        return links


async def add_link(full_link: str, creator: str) -> Links:
    async with async_session() as session:
        link = Links(full_link=full_link, creator=creator)
        session.add(link)
        await session.commit()
        session.refresh(link)
        return link


async def del_link(link_id: int) -> bool:
    async with async_session() as session:
        query: Links = select(Links).where(Links.id == link_id)
        link: Links = await session.scalar(query)
        if link is None:
            return False
        link.remove = True
        session.add(link)
        await session.commit()
        return True


async def find_short_link(full_link: str) -> Links:
    async with async_session() as session:
        query: Links = select(Links).where(Links.full_link == full_link)
        link: Links = await session.scalar(query)
        return link


async def find_full_link(short_link: int) -> Links:
    async with async_session() as session:
        query: Links = select(Links).where(Links.id == short_link)
        link: Links = await session.scalar(query)
        return link


async def add_crossings(link: Links, user: str) -> None:
    async with async_session() as session:
        crossings = Crossings(link=link, user=user)
        session.add(crossings)
        await session.commit()


async def get_crossings(short_link: int) -> str:
    async with async_session() as session:
        query: Crossings = (
            select(Crossings)
            .join(Crossings.link)
            .where(Links.id == short_link)
        )
        crossings: Crossings = (await session.scalars(query)).all()
        return crossings


# if __name__ == "__main__":
#     asyncio.run(create_model())
