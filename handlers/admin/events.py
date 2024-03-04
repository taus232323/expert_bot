from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.exceptions import TelegramForbiddenError

from settings import ADMIN_USER_IDS, TOKEN
from keyboards import inline, builders
from filters.is_admin import IsAdmin
from data.requests import (
    set_event, delete_event, edit_event, get_participants, get_event_by_id, get_events, get_paid_days, update_paid_days) 


router = Router()
scheduler = AsyncIOScheduler()
admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"


class AddEvent(StatesGroup):
    title = State()
    description = State()
    date = State()
    
    
class EditEvent(StatesGroup):
    _id = State()
    title = State()
    description = State()
    date = State()
    


@router.callback_query(IsAdmin(), F.data == "add_event")
async def add_more_event(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddEvent.title)
    await callback.message.edit_text(
        'Введите название события. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
        reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), AddEvent.title)
async def add_event_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    await state.set_state(AddEvent.description)
    await message.answer('Введите описание события', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), AddEvent.description)
async def add_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddEvent.date)
    await message.answer(f'Введите дату события в формате\nДД.ММ.ГГГГ ЧЧ:ММ', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), AddEvent.date)
async def add_event_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer(
            'Неверный формат даты и времени. Пожалуйста, введите дату и время события в формате\nДД.ММ.ГГГГ ЧЧ:ММ')
        return
    else:
        if date < datetime.now() + timedelta(days=1):
            await message.answer('Дата события не может быть раньше текущей даты и меньше чем за 24 часа после')
            return
        await state.update_data(date=date)
        data = await state.get_data()
        await set_event(data)
        await state.clear()
        await message.answer('Событие успешно добавлено', reply_markup=await builders.admin_get_events())
        await schedule_reminders()
    
@router.callback_query(IsAdmin(), F.data.startswith("predelete_event_"))
async def predelete_event_selected(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    warning = "Это действие удалит мероприятие вместе со списком участников, но Вы можете просто изменить его"
    await callback.message.edit_text(warning, reply_markup=await inline.confirm_delete_event(event_id))
    
@router.callback_query(IsAdmin(), F.data.startswith("delete_event_"))
async def delete_event_selected(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    await delete_event(event_id)
    await callback.answer("Мероприятие успешно удалено")
    markup = await builders.admin_get_events()
    num_buttons = sum(len(row) for row in markup.inline_keyboard)
    if num_buttons > 2: 
        await callback.message.edit_text("Мои самые интересные мероприятия", reply_markup=markup)    
    else:
        await callback.message.edit_text("У вас нет мероприятий", reply_markup=inline.new_event)
    
@router.callback_query(IsAdmin(), F.data.startswith("edit_event_"))
async def edit_event_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(_id=callback.data.split('_')[2])
    await state.set_state(EditEvent.title)
    await callback.message.edit_text(
        'Введите новое название события. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
        reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditEvent.title)
async def edit_event_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    await state.set_state(EditEvent.description)
    await message.answer('Введите описание события', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditEvent.description)
async def edit_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(EditEvent.date)
    await message.answer(f"Введите дату события в формате\nДД.ММ.ГГГГ ЧЧ:ММ", reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditEvent.date)
async def edit_event_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer(
            f'Неверный формат даты и времени. Пожалуйста, введите дату и время события в формате\nДД.ММ.ГГГГ ЧЧ:ММ')
        return
    else:
        if date < datetime.now()  + timedelta(days=1):
            await message.answer('Дата события не может быть раньше текущей даты и меньше чем за 24 часа после')
            return
        await state.update_data(date=date)
        data = await state.get_data()
        event_id = data['id']
        await remove_old_reminders(event_id)
        await edit_event(data)
        await state.clear()
        await message.answer('Событие успешно изменено', reply_markup=await builders.admin_get_events())
        await schedule_reminders()

async def remove_old_reminders(event_id):
    jobs = scheduler.get_jobs()
    for job in jobs:
        if job.args[0] == event_id:
            scheduler.remove_job(job.id)

@router.callback_query(IsAdmin(), F.data.startswith("participants_"))
async def check_participants(callback: CallbackQuery):
    event_id = callback.data.split("_")[1]
    participants = await get_participants(event_id)
    event = await get_event_by_id(event_id)
    if not participants:
        await callback.message.edit_text("Участников нет", reply_markup=inline.cancel_action)
    else:
        participant_text_list = []
        for i, participant in enumerate(participants, 1):
            username_or_id = participant.username if participant.username else participant.tg_id
            participant_text_list.append(f"{i}. @{username_or_id}")
            participant_text = "\n".join(participant_text_list)
            formatted_date = event.date.strftime('%d-%m-%Y %H:%M')
            message_text = (f"Пользователи записавшиеся на\n<b>{event.title}</b>,"
                    f"который состоится <b>{formatted_date}</b>:\n\n" + participant_text)
            await callback.message.edit_text(message_text, reply_markup=inline.participants_newsletter)

async def send_admin_reminder(event_id):
    bot = Bot(token=TOKEN, parse_mode='HTML')
    event = await get_event_by_id(event_id)
    participants = await get_participants(event_id)
    participant_text_list = []
    for i, participant in enumerate(participants, 1):
        username_or_id = participant.username if participant.username else participant.tg_id
        participant_text_list.append(f"{i}. @{username_or_id}")
    participant_text = "\n".join(participant_text_list)
    formatted_date = event.date.strftime('%d-%m-%Y %H:%M')
    message_text = (f"Пользователи записавшиеся на\n<b>{event.title}</b>,"
                    f"который состоится <b>{formatted_date}</b>:\n\n" + participant_text)
    for admin in ADMIN_USER_IDS:
        try:
            await bot.send_message(chat_id=admin, text=message_text, reply_markup=inline.participants_newsletter)
        except TelegramForbiddenError:
            print(f"Не удалось отправить уведомление админу {admin}")
    await bot.session.close() 

async def schedule_reminders():
    if scheduler.running:
        scheduler.shutdown(wait=False)
    upcoming_events = await get_events()
    for event in upcoming_events:
        if event.date <= datetime.now():
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
            scheduler.add_job(send_admin_reminder, evening_reminder_trigger, args=(event.id,))
        if not scheduler.running:
            scheduler.start()
            
            