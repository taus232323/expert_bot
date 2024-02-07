from app.database.models import async_session, User, Contacts, Events, Cases, Briefing, Services
from sqlalchemy import select, delete, update
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

async def set_contact(data):
    async with async_session() as session:
        session.add(Contacts(**data))
        await session.commit()  
        
async def get_contacts():
    async with async_session() as session:
        contacts = await session.scalars(select(Contacts))
        return contacts
    
async def delete_contacts():
    async with async_session() as session:
        contacts = await session.execute(select(Contacts))
        for contact in contacts.scalars().all():
            await session.delete(contact)
        await session.commit()
        
async def get_contact_by_id(id):
    async with async_session() as session:
        contact = await session.scalar(select(Contacts).where(Contacts.id == id))
        return contact
    
async def edit_contact(id):
    async with async_session() as session:
        contact = await session.scalar(select(Contacts).where(Contacts.id == id))
        session.update(Contacts(**data)
        await session.commit()
    
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
