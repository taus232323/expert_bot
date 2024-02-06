from app.database.models import async_session, User, Contacts, Events, Cases, Briefing, Services
from sqlalchemy import update

async def update_contacts(contact_id, new_contact_type, new_value) -> None:
    async with async_session() as session:
        stmt = (
            update(Contacts)
            .where(Contacts.id == contact_id)
            .values(
                contact_type=new_contact_type,
                value=new_value,
            )
        )
        await session.execute(stmt)
        await session.commit()


async def update_cases(case_id, new_title, new_description) -> None:
    async with async_session() as session:
        stmt = (
            update(Cases)
            .where(Cases.id == case_id)
            .values(title=new_title, description=new_description)
        )
        await session.execute(stmt)
        await session.commit()

async def update_events(event_id, new_name, new_description, new_date) -> None:
    async with async_session() as session:
        stmt = (
            update(Events)
            .where(Events.id == event_id)
            .values(name=new_name, description=new_description, date=new_date)
        )
        await session.execute(stmt)
        await session.commit()

async def update_services(service_id, new_name, new_description) -> None:
    async with async_session() as session:
        stmt = (
            update(Services)
            .where(Services.id == service_id)
            .values(name=new_name, description=new_description)
        )
        await session.execute(stmt)
        await session.commit()

async def update_briefing(briefing_id, new_instruction, new_questions, new_answers) -> None:
    async with async_session() as session:
        stmt = (
            update(Briefing)
            .where(Briefing.id == briefing_id)
            .values(instruction=new_instruction, questions=new_questions, answers=new_answers)
        )
        await session.execute(stmt)
        await session.commit()

async def update_user(user_id, new_tg_id, new_username, new_first_name, new_last_name) -> None:
    async with async_session() as session:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(tg_id=new_tg_id, username=new_username, first_name=new_first_name, last_name=new_last_name)
        )
        await session.execute(stmt)
        await session.commit()
