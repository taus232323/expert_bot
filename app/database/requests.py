from app.database.models import async_session, User, Contacts, Events, Cases, Briefing, Services
from sqlalchemy import select
from typing import List


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users
    
async def get_contacts():
    async with async_session() as session:
        result = await session.scalars(select(Contacts))
        return result
    
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
