from app.database.models import async_session, Users, Contacts, Events, Cases, Briefing, Services, Participants
from sqlalchemy import select, delete, update
from typing import List


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id, Users.username == username))
        if not user:
            session.add(Users(tg_id=tg_id, username=username))
            await session.commit()     
        
async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(Users))
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

async def delete_case(case_id: int):
    async with async_session() as session:
        await session.execute(delete(Cases).where(Cases.id == case_id))
        await session.commit()
        
async def edit_case(data):
    async with async_session() as session:
        await session.execute(
            update(Cases).where(Cases.id == data["id"]).values({
                Cases.title: data['title'],
                Cases.description: data['description']}))
        await session.commit()

async def get_services():
    async with async_session() as session:
        services = await session.scalars(select(Services))
        return services

async def get_service_by_id(service_id: int):
    async with async_session() as session:
        service = await session.scalar(select(Services).where(Services.id == service_id))
        return service

async def set_service(data):
    async with async_session() as session:
        session.add(Services(**data))
        await session.commit()
        
async def delete_service(service_id: int):
    async with async_session() as session:
        await session.execute(delete(Services).where(Services.id == service_id))
        await session.commit()
        
async def edit_service(data):
    async with async_session() as session:
        await session.execute(
            update(Services).where(Services.id == data["id"]).values({
                Services.title: data['title'],
                Services.description: data['description']}))
        await session.commit()

async def get_events():
    async with async_session() as session:
        events = await session.scalars(select(Events))
        return events
    
async def get_event_by_id(event_id: int):
    async with async_session() as session:
        event = await session.scalar(select(Events).where(Events.id == event_id))
        return event
    
async def set_event(data):
    async with async_session() as session:
        session.add(Events(**data))
        await session.commit()

async def delete_event(event_id: int):
    async with async_session() as session:
        await session.execute(delete(Events).where(Events.id == event_id))
        await session.commit()

async def edit_event(data):
    async with async_session() as session:
        await session.execute(
            update(Events).where(Events.id == data["id"]).values({
                Events.title: data['title'],
                Events.description: data['description'],
                Events.date: data['date']}))
        await session.commit()

async def set_participant(tg_id, event_id):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        participants = await session.execute(select(Participants).where(Participants.event == event_id))
        if participants is None:
            session.add(Participants(users=user.id, event=event_id))
        else:
            await session.execute(update(Participants).where(Participants.event == event_id).values(users=user.id))
        await session.commit()
        
async def check_participant(event_id, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        participants = await session.scalar(select(Participants).where(Participants.event == event_id, Participants.users == user.id))
        if participants:
            return True
        else:
            return False
        
        
async def get_participants(event_id: int):
    async with async_session() as session:
        participants = await session.scalar(select(Participants).where(Participants.event == event_id))
        if participants is not None:
            users = await session.scalars(select(Users).where(Users.id == participants.users))
            return users

        

        
