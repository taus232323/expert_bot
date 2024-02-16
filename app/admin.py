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

contact_type_hint = (
"Введите тип контактной информации. Например: ФИО; Телефон; Адрес; График"
"работы; Ссылка на сайт, или социальные сети"
)
admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации"
     
class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN_USER_IDS
     
                                     
class Newsletter(StatesGroup):
    message = State()


class AddWelcome(StatesGroup):
    picture = State()
    about = State()


class EditWelcome(StatesGroup):
    id = State()
    picture = State()
    about = State()


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


class EditInstruction(StatesGroup):
    id = State()
    description = State()
    
    
class AddBriefing(StatesGroup):
    question = State()
    answer = State()


class EditBriefing(StatesGroup):
    id = State()
    question = State()
    answer = State()
    
    
@admin.message(AdminProtect(), F.text == "Приветствие")    
async def welcome_selected(message: Message):
    welcome = await get_welcome()
    if len(welcome) < 2:
        await message.answer('Вы ещё не добавили приветственного сообщения. Хотите сделать это сейчас?',
                             reply_markup=kb.new_welcome)
    else:
        await message.answer_photo(welcome.picture, welcome.about, reply_markup=kb.edit_welcome)

@admin.callback_query(AdminProtect(), F.data == "new_welcome")
async def new_welcome(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Для начала отправьте своё самое лучшее фото',
                                     reply_markup=kb.cancel_action)
    await  state.set_state(AddWelcome.picture)

@admin.message(AdminProtect(), AddWelcome.picture)
async def add_welcome_picture(message: Message, state: FSMContext):
    await state.update_data(picture=message.photo[-1].file_id)
    await state.set_state(AddWelcome.about)
    await message.answer(
    'Теперь расскажите вкратце кто Вы  и чем занимаетесь. Остальное мы позже добавим в соответствующие пункты меню', 
                        reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), AddWelcome.about)
async def add_welcome_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()
    await set_welcome(data)
    await state.clear()
    await message.answer(
        'Приветственное сообщение успешно добавлено. Теперь можно добавить информацию в другие пункты меню ниже', 
        reply_markup=kb.admin_main)
    
@admin.callback_query(AdminProtect(), F.data == "edit_welcome")
async def edit_welcome(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Пришлите фото которое ещё лучше предыдущего', reply_markup=kb.cancel_action)
    await state.set_state(EditWelcome.picture)
    
@admin.message(AdminProtect(), EditWelcome.picture)
async def edit_welcome_picture(message: Message, state: FSMContext):
    await state.update_data(picture=message.photo[-1].file_id)
    await state.set_state(EditWelcome.about)
    await message.answer(
        'Теперь добавьте более актуальную и интересную информацию о себе', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditWelcome.about)
async def edit_welcome_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()
    await set_welcome(data)
    await state.clear()
    await message.answer(
        'Приветственное сообщение успешно изменено. Теперь можно добавить информацию в другие пункты меню ниже',
        reply_markup=kb.admin_main)
    
@admin.callback_query(AdminProtect(), F.data == "add_contact")
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
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", reply_markup=kb.contacts)
    
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
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", 
                         reply_markup=kb.contacts)
    
@admin.callback_query(AdminProtect(), F.data == "delete_contact")
async def delete_contact(callback: CallbackQuery):
    await callback.message.edit_text("Эта операция удалит всю контактную информацию. Вы уверены?",
                                  reply_markup=kb.confirm_delete_contacts)
    
@admin.callback_query(AdminProtect(), F.data == "confirmed_delete_contacts")
async def confirm_delete_contact(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await delete_contacts()
    await callback.answer("Контактная информацию успешно удалена")    
    
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
    
@admin.callback_query(AdminProtect(), F.data.startswith("predelete_event_"))
async def predelete_event_selected(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    warning = "Это действие удалит мероприятие вместе со списком участников, но Вы можете просто изменить его"
    await callback.answer(warning, reply_markup=kb.confirm_delete_event_keyboard())
    
@admin.callback_query(AdminProtect(), F.data.startswith("delete_event_"))
async def delete_event_selected(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    await delete_event(event_id)
    await callback.answer("Мероприятие успешно удалено")
    await callback.message.edit_text("Мои самые интересные мероприятия", reply_markup=await kb.admin_get_events_keyboard())    
    
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

@admin.callback_query(AdminProtect(), F.data == "instruction")
async def instruction(callback: CallbackQuery):
    instructions = await get_instructions()
    default_instruction = f"<b>Вы не добавили инструкцию. По умолчанию она такая:</b>\n Этот брифинг создан, чтобы упростить наше будущее сотрудничество и не займет много Вашего времени"
    if instructions:
        instr_text = f"{instructions.description if instructions else None}"
        await callback.message.edit_text(instr_text, reply_markup=kb.edit_instruction)
    else:
        instr_text = default_instruction        
        await callback.message.edit_text(instr_text, reply_markup=kb.new_instruction)

@admin.callback_query(AdminProtect(), F.data == "add_instruction")
async def add_instruction(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddInstruction.description)
    await callback.message.edit_text('Введите свою инструкцию по прохождению брифинга', reply_markup=kb.cancel_action)

@admin.message(AdminProtect(), AddInstruction.description)
async def save_instruction(message: Message, state: FSMContext):
    await delete_instructions()
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_instructions(data)
    await state.clear()
    await message.answer("Инструкция сохранена. Теперь можно приступить к созданию брифнга", 
                         reply_markup=kb.in_create_briefing) 

@admin.callback_query(AdminProtect(), F.data == "edit_instruction")
async def edit_instruction(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddInstruction.description)
    await callback.message.edit_text('Введите новую инструкцию по прохождению брифинга', reply_markup=kb.cancel_action)
    
@admin.callback_query(AdminProtect(), F.data == "delete_instruction")
async def delete_instruction(callback: CallbackQuery):
    await delete_instructions()
    await callback.message.edit_text('Инструкция удалена', reply_markup=kb.admin_get_briefing)

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
                         reply_markup=kb.in_create_briefing)

@admin.callback_query(AdminProtect(), F.data == "add_question")
async def add_question_to_briefing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Давайте добавим ещё один вопрос')
    await asyncio.sleep(1)
    await state.set_state(AddBriefing.question)
    await callback.message.edit_text('Введите текст вопроса', reply_markup=kb.cancel_action)

@admin.callback_query(AdminProtect(), F.data == "edit_briefing")
async def edit_briefing(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.answer('Хотите добавить новый вопрос, изменить существующий или удалить брифинг целиком?', 
                                     reply_markup=kb.edit_briefing)

@admin.callback_query(AdminProtect(), F.data == "predelete_briefing")
async def predelete_briefing(callback: CallbackQuery):
    warning = 'Эта операция удалит весь брифинг вместе с ответами пользователей, '
    'но вы можете изменить вопросы по отдельности'
    await callback.message.edit_text(warning, reply_markup=kb.confirm_delete_briefing)
    
@admin.callback_query(AdminProtect(), F.data == "delete_briefing")
async def delete_briefing(callback: CallbackQuery):
    await delete_briefing()
    await callback.message.edit_text('Брифинг удалён', reply_markup=kb.in_create_briefing)

@admin.callback_query(AdminProtect(), F.data == "edit_question")
async def edit_question_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditBriefing.id)
    await callback.message.edit_text('Введите номер вопроса, который Вы желаете изменить', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditBriefing.id)
async def edit_question(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    await state.set_state(EditBriefing.question)
    await message.answer('Введите новый вопрос', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditBriefing.question)
async def edit_question_text(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(EditBriefing.answer)
    await message.answer('Введите новый ответ', reply_markup=kb.cancel_action)
    
@admin.message(AdminProtect(), EditBriefing.answer)
async def edit_question_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    await edit_question(data)
    await state.clear()
    await message.answer('Вопрос изменён. Хотите посмотреть что получилось или добавить ещё один?', 
                         reply_markup=kb.in_create_briefing)

@admin.message(AdminProtect(), Command('newsletter'))
@admin.callback_query(AdminProtect(), F.data == "newsletter")
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям', 
                         reply_markup=kb.cancel_action)
    
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
    await callback.message.answer(admin_hint, reply_markup=kb.admin_main)
    