from app.database.models import async_session, User, Contacts, Events, Cases, Briefing, Services, WebsiteLinks
from sqlalchemy import select
from typing import List


async def get_contacts() -> List[Contacts]:
    async with async_session() as session:
        result = await session.scalars(select(Contacts))
        return result

async def get_links(link_id) -> List[WebsiteLinks]:
    async with async_session() as session:
        result = await session.get(WebsiteLinks, link_id)
        return [result] if result else []

    
async def get_cases() -> List[Cases]:
    async with async_session() as session:
        result = await session.scalar(select(Cases))
        return result

async def get_events() -> List[Events]:
    async with async_session() as session:
        result = await session.scalar(select(Events))
        return result

async def get_services() -> List[Services]:
    async with async_session() as session:
        result = await session.scalars(select(Services))
        return result
    
async def get_briefing() -> List[Briefing]:
    async with async_session() as session:
        result = await session.scalars(select(Briefing))
        return result

async def get_user(user_id) -> User:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.id == user_id))
        return result
