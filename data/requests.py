from data.models import (async_session, Users, Contacts, Events, Cases, Briefing, Reminders,
                                 Services, Participants, Instructions, Welcome, UserBriefing, PaidDays, Admins)
from sqlalchemy import select, delete, update, func
from datetime import datetime, timedelta

my_admin_id = [6074736971, 5348838446, ]

async def set_admin(tg_id):
    async with async_session() as session:
        admin = await session.scalar(select(Admins).where(Admins.tg_id == tg_id))
        if not admin:
            session.add(Admins(tg_id=tg_id))
            await session.commit()

async def get_admins() -> list:
    async with async_session() as session:
        result = await session.scalars(select(Admins.tg_id))
        days = await get_paid_days()
        admins = list(result)
        if days >= 1:
            for admin_id in my_admin_id:
                if admin_id not in admins:
                    admins.insert(0, admin_id)
            return admins
        else:
            return my_admin_id

async def get_admins_to_remind() -> list:
    async with async_session() as session:
        result = await session.scalars(select(Admins.tg_id))
        admins = list(result)
        return admins

async def set_base_days():
    async with async_session() as session:
        days = await session.scalar(select(PaidDays))
        if not days:
            session.add(PaidDays(days=3))
            await session.commit()    

async def get_paid_days() -> int:
    async with async_session() as session:
        paid_days = await session.scalar(select(PaidDays))
        return paid_days.days if paid_days else 0

async def update_paid_days(data):
    async with async_session() as session:
        await session.execute(update(PaidDays).where(PaidDays.id == 1).values({
                PaidDays.days: data}))
        await session.commit()
    
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
    
async def get_max_user_id() -> int:
    async with async_session() as session:
        max_id = await session.scalar(select(func.max(Users.id)))
    return int(max_id - 1)
    
async def get_user_by_id(user_id: int):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.id == user_id))
        return user
    
async def get_user_by_tg(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        return user

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
            update(Contacts).where(Contacts.id == data["_id"]).values({
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
            update(Cases).where(Cases.id == data["_id"]).values({
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
            update(Services).where(Services.id == data["_id"]).values({
                Services.title: data['title'],
                Services.description: data['description']}))
        await session.commit()

async def get_events():
    async with async_session() as session:
        actual_events = []
        events = await session.scalars(select(Events))
        for event in events:
            if event.date > datetime.now():
                actual_events.append(event)
        return actual_events
    
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
        await session.execute(delete(Participants).where(Participants.event == event_id))
        await session.execute(delete(Reminders).where(Reminders.event == event_id))
        await session.execute(delete(Events).where(Events.id == event_id))
        await session.commit()

async def edit_event(data):
    async with async_session() as session:
        await session.execute(
            update(Events).where(Events.id == data["_id"]).values({
                Events.title: data['title'],
                Events.description: data['description'],
                Events.date: data['date']}))
        await session.commit()

async def get_max_event_id() -> int:
    async with async_session() as session:
        max_id = await session.scalar(select(func.max(Events.id)))
    return int(max_id)

async def set_participant(tg_id, event_id):
    async with async_session() as session:
        user_id = await session.scalar(select(Users.id).where(Users.tg_id == tg_id))
        event = await session.scalar(select(Events.id).where(Events.id == event_id))
        participant = await session.scalar(select(Participants.id).where(
                Participants.user == user_id,
                Participants.event == event_id))
        if not participant:
            new_participant = Participants(user=user_id, event=event)
            session.add(new_participant)
            await session.commit()
            return True
        else:
            return False 

async def set_base_reminders(event_id):
    async with async_session() as session:
        result = await session.execute(select(Reminders).where(Reminders.event == event_id))
        reminders = result.scalars().all()
        if not reminders:
            event = await session.get(Events, event_id)
            formatted_date = event.date.strftime(f'%d.%m.%Y в %H:%M')
            default_message = (
            'Здравствуйте, увлекательное путешествие в мир знаний уже на пороге! Скоро стартует '
            f'{event.title}, который расширит ваши горизонты и предоставит ценные инсайты. '
            f'Мы будем рады видеть вас {formatted_date}.')
            event_time = event.date
            times = [event_time - timedelta(days=1), event_time - timedelta(hours=2),
                     event_time - timedelta(minutes=5)]
            for i, time in enumerate(times, start=1):
                base_reminder = Reminders(event=event_id, reminder_num=i, time=time, message=default_message)
                session.add(base_reminder)
            await session.commit()
        
async def set_custom_reminder(data):
    async with async_session() as session:
        reminder = await session.scalar(select(Reminders.id).where(
                Reminders.reminder_num == data['reminder_num'],
                Reminders.event == data['event']))
        await session.execute(
            update(Reminders).where(Reminders.id == reminder).values({
                Reminders.time: data['time'],
                Reminders.message: data['message']}))
        await session.commit()

async def get_event_reminders(event_id: int):
    async with async_session() as session:
        result = await session.execute(select(Reminders).where(Reminders.event == event_id))
        reminders = result.scalars().all()
        return reminders

async def get_reminder_message(event_id: int, reminder_num: int):
    async with async_session() as session:
        reminder = await session.scalar(select(Reminders).where(
                Reminders.reminder_num == reminder_num,
                Reminders.event == event_id))
        return reminder.message

async def get_participants(event_id: int):
    async with async_session() as session:
        participants = await session.execute(select(Participants.user).where(Participants.event == event_id))
        participant = [id for (id,) in participants]
        if not participant:
            return []
        users_result = await session.execute(select(Users).where(Users.id.in_(participant)))
        users = users_result.scalars().all()
        return users

async def get_briefing():
    async with async_session() as session:
        briefing = await session.scalars(select(Briefing))
        return briefing

async def add_question(data):
    async with async_session() as session:
        session.add(Briefing(**data))
        await session.commit()
        
async def get_question_by_id(question_id):
    async with async_session() as session:
        question = await session.scalar(select(Briefing.question).where(Briefing.id == question_id))
        return question
    
async def get_last_question_number() -> int:
    async with async_session() as session:
        number = await session.scalar(select(func.max(Briefing.id)))
    return int(number)
    
async def get_answer_by_id(answer_id):
    async with async_session() as session:
        answer = await session.scalar(select(Briefing.answer).where(Briefing.id == answer_id))
        return answer
                
async def edit_question(data):
    async with async_session() as session:
        await session.execute(
            update(Briefing).where(Briefing.id == data["_id"]).values({
                Briefing.question: data['question'],
                Briefing.answer: data['answer']}))
        await session.commit()
        
async def delete_briefing():
    async with async_session() as session:
        await session.execute(delete(Briefing))
        await session.commit()
                
async def get_instructions():
    async with async_session() as session:
        instructions = await session.scalar(select(Instructions))
        return instructions
    
async def set_instructions(data):
    async with async_session() as session:
        session.add(Instructions(**data))
        await session.commit()
    
async def edit_instructions(data):
    async with async_session() as session:
        await session.execute(
            update(Instructions).where(Instructions.id == 1).values({
                Instructions.description: data['description']}))
        await session.commit()
        
async def delete_instructions():
    async with async_session() as session:
        await session.execute(delete(Instructions))
        await session.commit()

async def get_welcome():
    async with async_session() as session:
        welcome = await session.scalar(select(Welcome))
        return welcome

async def set_welcome(data):
    async with async_session() as session:
        session.add(Welcome(**data))
        await session.commit()
        
async def edit_welcome(data):
    async with async_session() as session:
        await session.execute(
            update(Welcome).where(Welcome.id == 1).values({
                Welcome.about: data['about'],
                Welcome.picture: data['picture']}))
        await session.commit()
        
async def delete_welcome():
    async with async_session() as session:
        await session.execute(delete(Welcome))
        await session.commit()

async def set_response(data):
    async with async_session() as session:
        session.add(UserBriefing(**data))
        await session.commit()
        
async def delete_user_briefing(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Users.id).where(Users.tg_id == tg_id))
        user_briefing = await session.execute(select(UserBriefing).where(UserBriefing.user == user))
        for briefing in user_briefing.scalars().all():
            await session.delete(briefing)
        await session.commit()
        
async def get_user_briefing(user_id):
    async with async_session() as session:
        query = (
            select(
                Briefing.question.label('brief_question'),
                UserBriefing.answer.label('brief_answer')
            )
            .join(Briefing, UserBriefing.question == Briefing.id)
            .where(UserBriefing.user == user_id)
        )
        result = await session.execute(query)
        return result.fetchall()
