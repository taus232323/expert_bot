from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.exceptions import TelegramForbiddenError
import asyncio


from settings import ADMIN_USER_IDS, TOKEN

import app.keyboards as kb
from app.database.requests import (
get_users, set_contact, get_contacts, delete_contacts, edit_contact, set_case, delete_case, edit_case,
set_service, delete_service, edit_service, set_event, delete_event, edit_event, get_participants, 
get_event_by_id, get_events, set_instructions, edit_instructions, delete_instructions, get_briefing,
get_question_by_id, add_question, edit_question, get_welcome, set_welcome, edit_welcome, delete_welcome, 
get_instructions, delete_briefing
)

admin = Router()
scheduler = AsyncIOScheduler()

contact_type_hint = "Введите тип контактной информации. Например: Фамилия, Имя, Отчество; Телефон; Адрес офиса; График работы; Ссылка на сайт, или социальные сети (Вводить по одной ссылке)"
admin_hint = f"Возможные команды:\n\n/newsletter - Сделать рассылку\n\n/add_contact - Добавить контактную информацию\n\n/add_case - Добавить Кейс\n\n/add_event - Добавить Мероприятие\n\n/add_service - Добавить Услугу\n\n/create_briefing - Создать брифинг"
     
class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN_USER_IDS
     
                                     
class Newsletter(StatesGroup):
    message = State()


class AddContact(StatesGroup):
    contact_type = State()
    contact_value = State()


class EditContact(StatesGroup):
    id = State()
    contact_type = State()
    contact_value = State()


class AddCase(StatesGroup):
    title = State()
    description = State()
    
    
class EditCase(StatesGroup):
    id = State()
    title = State()
    description = State()
        
        
class AddService(StatesGroup):
    title = State()
    description = State()
    

class EditService(StatesGroup):
    id = State()
    title = State()
    description = State()

class AddEvent(StatesGroup):
    title = State()
    description = State()
    date = State()
    
    
class EditEvent(StatesGroup):
    id = State()
    title = State()
    description = State()
    date = State()
    

class AddInstruction(StatesGroup):
    description = State()


class AddBriefing(StatesGroup):
    question = State()
    answer = State()


class EditBriefing(StatesGroup):
    id = State()
    question = State()
    answer = State()
    

@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message):
    await message.answer(admin_hint)

@admin.message(AdminProtect(), Command('add_contact'))
async def add_contact(message: Message, state: FSMContext):
    await state.set_state(AddContact.contact_type)
    await message.answer(contact_type_hint, reply_markup=kb.cancel_action)
    
@admin.callback_query(AdminProtect(), F.data =="add_contact")
async def add_more_contact(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddContact.contact_type)
    await callback.message.edit_text(contact_type_hint, reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddContact.contact_type)
async def add_contact_type(message: Message, state: FSMContext):
    await state.update_data(contact_type=message.text)
    await state.set_state(AddContact.contact_value)
    await message.answer('Введите контактную информацию', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddContact.contact_value)
async def add_contact_value(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await set_contact(data)
    await state.clear()
    await message.answer('Контактная информация успешно добавлена')
    contacts = await get_contacts()   
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", reply_markup=kb.contacts_kb)
    
@admin.callback_query(AdminProtect(), F.data == "edit_contacts")
async def edit_contacts(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите контактную для изменения", 
                                  reply_markup=await kb.edit_contact_kb())
    
@admin.callback_query(AdminProtect(), F.data.startswith("edit_contact_"))
async def edit_contact_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=callback.data.split('_')[2])
    await state.set_state(EditContact.contact_type)
    await callback.message.edit_text(contact_type_hint, reply_markup=kb.cancel_action)
   
@admin.message(AdminProtect(), EditContact.contact_type)
async def edit_contact_type(message: Message, state: FSMContext):
    await state.update_data(contact_type=message.text)
    await state.set_state(EditContact.contact_value)
    await message.answer('Введите контактную информацию', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditContact.contact_value)
async def edit_contact_value(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await edit_contact(data)
    await state.clear()
    await message.answer('Контактная информация успешно изменена')
    contacts = await get_contacts()
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", reply_markup=kb.contacts_kb)
    
@admin.callback_query(AdminProtect(), F.data == "delete_contact")
async def delete_contact(callback: CallbackQuery):
    await callback.message.edit_text("Эта операция удалит всю контактную информацию. Вы уверены?",
                                  reply_markup=kb.confirm_delete_contacts)
    
@admin.callback_query(AdminProtect(), F.data == "confirmed_delete_contacts")
async def confirm_delete_contact(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await delete_contacts()
    await callback.answer("Контактная информацию успешно удалена")    

@admin.message(AdminProtect(), Command('add_case'))
async def add_case(message: Message, state: FSMContext):
    await state.set_state(AddCase.title)
    await message.answer('Введите название кейса', reply_markup=kb.cancel_action)
    
@admin.callback_query(AdminProtect(), F.data == "add_case")
async def add_more_case(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCase.title)
    await callback.message.edit_text('Введите название кейса', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddCase.title)
async def add_case_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddCase.description)
    await message.answer('Введите описание кейса', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddCase.description)
async def add_case_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_case(data)
    await state.clear()
    await message.answer('Кейс успешно добавлен', reply_markup=await kb.admin_get_cases_keyboard())

@admin.callback_query(AdminProtect(), F.data.startswith("delete_case_"))
async def delete_case_selected(callback: CallbackQuery):
    await delete_case(callback.data.split('_')[2])
    await callback.answer("Кейс успешно удалён")
    await callback.message.edit_text("Мои самые лучшие кейсы", reply_markup=await kb.admin_get_cases_keyboard())
    
@admin.callback_query(AdminProtect(), F.data.startswith("edit_case_"))
async def edit_case_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=callback.data.split('_')[2])
    await state.set_state(EditCase.title)
    await callback.message.edit_text('Введите название кейса', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditCase.title)
async def edit_case_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(EditCase.description)
    await message.answer('Введите описание кейса', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), EditCase.description)
async def edit_case_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await edit_case(data)
    await state.clear()
    await message.answer('Кейс успешно изменён', reply_markup=await kb.admin_get_cases_keyboard())

@admin.message(AdminProtect(), Command('add_service'))
async def add_service(message: Message, state: FSMContext):
    await state.set_state(AddService.title)
    await message.answer('Введите название услуги', reply_markup=kb.cancel_action)
    
@admin.callback_query(AdminProtect(), F.data == "add_service")
async def add_more_service(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddService.title)
    await callback.message.edit_text('Введите название услуги', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddService.title)
async def add_service_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddService.description)
    await message.answer('Введите описание услуги', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddService.description)
async def add_service_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_service(data)
    await state.clear()
    await message.answer('Услуга успешно добавлена', reply_markup=await kb.admin_get_services_keyboard())

@admin.callback_query(AdminProtect(), F.data.startswith("delete_service_"))
async def delete_service_selected(callback: CallbackQuery):
    await delete_service(callback.data.split('_')[2])
    await callback.answer("Услуга успешно удалена")
    await callback.message.edit_text("Мои самые выгодные услуги", reply_markup=await kb.admin_get_services_keyboard())

@admin.callback_query(AdminProtect(), F.data.startswith("edit_service_"))
async def edit_service_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=callback.data.split('_')[2])
    await state.set_state(EditService.title)
    await callback.message.edit_text('Введите название услуги', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditService.title)
async def edit_service_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(EditService.description)
    await message.answer('Введите описание услуги', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditService.description)
async def edit_service_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await edit_service(data)
    await state.clear()
    await message.answer('Услуга успешно изменена', reply_markup=await kb.admin_get_services_keyboard())

@admin.message(AdminProtect(), Command('add_event'))
async def add_event(message: Message, state: FSMContext):
    await state.set_state(AddEvent.title)
    await message.answer('Введите название события', reply_markup=kb.cancel_action)
    
@admin.callback_query(AdminProtect(), F.data == "add_event")
async def add_more_event(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddEvent.title)
    await callback.message.edit_text('Введите название события', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddEvent.title)
async def add_event_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddEvent.description)
    await message.answer('Введите описание события', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddEvent.description)
async def add_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddEvent.date)
    await message.answer('Введите дату события в формате ДД.ММ.ГГГГ ЧЧ:ММ', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddEvent.date)
async def add_event_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer('Неверный формат даты и времени. Пожалуйста, введите дату и время события в формате ДД.ММ.ГГГГ ЧЧ:ММ')
        return
    else:
        if date < datetime.now() + timedelta(days=1):
            await message.answer('Дата события не может быть раньше текущей даты и меньше чем за 24 часа после')
            return
        await state.update_data(date=date)
        data = await state.get_data()
        await set_event(data)
        await state.clear()
        await message.answer('Событие успешно добавлено', reply_markup=await kb.admin_get_events_keyboard())
        await schedule_reminders()
    
@admin.callback_query(AdminProtect(), F.data.startswith("delete_event_"))
async def delete_event_selected(callback: CallbackQuery):
    await delete_event(callback.data.split('_')[2])
    await callback.answer("Событие успешно удалено")
    await callback.message.edit_text("Мои самые интересные события", reply_markup=await kb.admin_get_events_keyboard())
    
@admin.callback_query(AdminProtect(), F.data.startswith("edit_event_"))
async def edit_event_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=callback.data.split('_')[2])
    await state.set_state(EditEvent.title)
    await callback.message.edit_text('Введите название события', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditEvent.title)
async def edit_event_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(EditEvent.description)
    await message.answer('Введите описание события', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditEvent.description)
async def edit_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(EditEvent.date)
    await message.answer('Введите дату события в формате ДД.ММ.ГГГГ ЧЧ:ММ', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditEvent.date)
async def edit_event_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer('Неверный формат даты и времени. Пожалуйста, введите дату и время события в формате ДД.ММ.ГГГГ ЧЧ:ММ')
        return
    else:
        if date < datetime.now()  + timedelta(days=1):
            await message.answer('Дата события не может быть раньше текущей даты и меньше чем за 24 часа после')
            return
        await state.update_data(date=date)
        data = await state.get_data()
        await edit_event(data)
        await state.clear()
        await message.answer('Событие успешно изменено', reply_markup=await kb.admin_get_events_keyboard())
        await schedule_reminders()

@admin.callback_query(AdminProtect(), F.data.startswith("participants_"))
async def check_participants(callback: CallbackQuery):
    event_id = callback.data.split("_")[1]
    participants = await get_participants(event_id)
    event = await get_event_by_id(event_id)
    if not participants:
        await callback.message.edit_text("Участников нет")
    else:
        participant_text_list = []
        for i, participant in enumerate(participants, 1):
            username_or_id = participant.username if participant.username else participant.tg_id
            participant_text_list.append(f"{i}. @{username_or_id}")
            participant_text = "\n".join(participant_text_list)
            formatted_date = event.date.strftime('%Y-%m-%d %H:%M')
            message_text = (f"Пользователи записавшиеся на\n<b>{event.title}</b>,"
                    f"который состоится <b>{formatted_date}</b>:\n\n" + participant_text)
            await callback.message.edit_text(message_text, reply_markup=kb.participants_newsletter)

async def send_admin_reminder(event_id):
    bot = Bot(token=TOKEN, parse_mode='HTML')
    event = await get_event_by_id(event_id)
    participants = await get_participants(event_id)
    participant_text_list = []
    for i, participant in enumerate(participants, 1):
        username_or_id = participant.username if participant.username else participant.tg_id
        participant_text_list.append(f"{i}. @{username_or_id}")
    participant_text = "\n".join(participant_text_list)
    formatted_date = event.date.strftime('%Y-%m-%d %H:%M')
    message_text = (f"Пользователи записавшиеся на\n<b>{event.title}</b>,"
                    f"который состоится <b>{formatted_date}</b>:\n\n" + participant_text)
    for admin in ADMIN_USER_IDS:
        try:
            await bot.send_message(chat_id=admin, text=message_text, reply_markup=kb.participants_newsletter)
        except TelegramForbiddenError:
            print(f"Не удалось отправить уведомление админу {admin}")
    await bot.session.close()

async def schedule_reminders():
    upcoming_events = await get_events()
    for event in upcoming_events:
        event_time = event.date
        if event_time - timedelta(days=1) > datetime.now():
            scheduler.add_job(send_admin_reminder, 'date', 
                              run_date=event_time - timedelta(days=1), 
                              args=(event.id,))
        elif event_time - timedelta(hours=3) > datetime.now():
            scheduler.add_job(send_admin_reminder, 'date',
                              run_date=event_time - timedelta(hours=3),
                              args=(event.id,))
        elif event_time - timedelta(minutes=30) > datetime.now():
            scheduler.add_job(send_admin_reminder, 'date',
                              run_date=event_time - timedelta(minutes=30),
                              args=(event.id,))
        evening_reminder_trigger = CronTrigger(hour=19, minute=0)
        scheduler.add_job(send_admin_reminder, evening_reminder_trigger, args=(event.id))
    scheduler.start()

@admin.callback_query(AdminProtect(), F.data == "add_instruction")
async def add_instruction(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddInstruction.description)
    await callback.message.edit_text('Введите описание инструкции', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddInstruction.description)
async def save_instruction(message: Message, state: FSMContext):
    await delete_instructions()
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_instructions(data)
    await state.clear()
    await message.answer("Инструкция сохранена. Теперь можно приступить к созданию брифнга", 
                         reply_markup=kb.in_create_briefing_kb) 


@admin.callback_query(AdminProtect(), F.data == "create_briefing")
async def create_briefing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Сейчас Вы будете создавать брифинг следуйте моим инструкциям и у Вас всё получится')
    await state.set_state(AddBriefing.question)
    await callback.message.answer('Введите текст вопроса', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddBriefing.question)
async def add_briefing_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(AddBriefing.answer)
    await message.answer('Введите варианты ответов через знак точки с запятой ";", либо знак минус '
                         '"-" если хотите, чтобы ответ был в свободной форме', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddBriefing.answer)    
async def add_briefing_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    await add_question(data)
    await state.clear()
    await message.answer("Вопрос добавлен. Хотите посмотреть что получилось или добавить ещё один?",
                         reply_markup=kb.in_create_briefing_kb)

@admin.callback_query(AdminProtect(), F.data == "add_question")
async def add_question_to_briefing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Давайте добавим ещё один вопрос')
    await asyncio.sleep(1)
    await state.set_state(AddBriefing.question)
    await callback.message.edit_text('Введите текст вопроса', reply_markup=kb.cancel_action)




@admin.message(AdminProtect(), Command('newsletter'))
@admin.callback_query(AdminProtect(), F.data == "newsletter")
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям', reply_markup=kb.cancel_action)
    

@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка.')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Рассылка успешно завершена.')
    await state.clear()

@admin.callback_query(AdminProtect(), F.data.startswith("cancel_"))
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await state.clear()
    await callback.answer("Операция отменена")
    await callback.message.answer(admin_hint)