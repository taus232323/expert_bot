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

async def get_contacts():
    async with async_session() as session:
        contacts = await session.scalars(select(Contacts))
        return contacts

async def set_contact(data):
    async with async_session() as session:
        session.add(Contacts(**data))
        await session.commit()  
    
async def delete_contacts():
    async with async_session() as session:
        contacts = await session.execute(select(Contacts))
        for contact in contacts.scalars().all():
            await session.delete(contact)
        await session.commit()
    
async def edit_contact(data):
    async with async_session() as session:
        await session.execute(
            update(Contacts).where(Contacts.id == data["id"]).values({
                Contacts.contact_type: data['contact_type'],
                Contacts.value: data['value']}))
        await session.commit()
    
async def get_cases():
    async with async_session() as session:
        cases = await session.scalars(select(Cases))
        return cases
    
async def get_case_by_id(case_id: int):
    async with async_session() as session:
        case = await session.scalar(select(Cases).where(Cases.id == case_id))
        return case
    
async def set_case(data):
    async with async_session() as session:
        session.add(Cases(**data))
        await session.commit()

async def delete_case(case_id):
    async with async_session() as session:
        case = await session.execute(select(Cases).where(Cases.id == case_id))
        await session.execute(delete(case))
        await session.commit()

async def edit_case(data):
    async with async_session() as session:
        await session.execute(
            update(Cases).where(Cases.id == data["id"]).values({
                Cases.name: data['title'],
                Cases.description: data['description']}))
        await session.commit()





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
