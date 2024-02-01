from app.database.models import async_session, User, Contacts, Events, Cases, Briefing, Services, WebsiteLinks
from sqlalchemy import select


async def get_contacts() -> list[Contacts]:
    async with async_session() as session:
        result = await session.scalars(select(Contacts))
        return result

async def get_links(link_id) -> WebsiteLinks:
    async with async_session() as session:
        result = await session.scalars(select(WebsiteLinks).where(WebsiteLinks.id == link_id))
        return result
    
async def get_cases() -> list[Cases]:
    async with async_session() as session:
        result = await session.scalar(select(Cases))
        return result

async def get_events() -> list[Events]:
    async with async_session() as session:
        result = await session.scalar(select(Events))
        return result

async def get_services() -> list[Services]:
    async with async_session() as session:
        result = await session.scalars(select(Services))
        return result
    
async def get_briefing() -> list[Briefing]:
    async with async_session() as session:
        result = await session.scalars(select(Briefing))
        return result

async def get_user(user_id) -> User:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.id == user_id))
        return result
