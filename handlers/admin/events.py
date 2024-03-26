from contextlib import suppress

from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.exceptions import TelegramForbiddenError

from settings import TOKEN
from keyboards import inline, builders, reply
from filters.is_admin import IsAdmin
from data.requests import (
    set_event, delete_event, edit_event, get_participants, get_event_by_id, get_admins, get_max_event_id,
    set_base_reminders, set_custom_reminder, get_event_reminders, get_events, get_reminder_message,
    get_users, get_max_user_id) 


router = Router()
events_scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"
reminder_hint = (
            f'⚠️ Теперь вы можете создать сообщение для рассылки пользователям записавшимся на мероприятие.\n\n'
            f'<b>По умолчанию оно такое:</b>\n\nЗдравствуйте, увлекательное путешествие в мир знаний уже '
            'на пороге! Скоро стартует [название мероприятия], который расширит ваши горизонты и '
            'предоставит ценные инсайты. Мы будем рады видеть вас [дата и время]'
            f'\n\n⚠️ Вы можете оставить такое уведомление, которое получат пользователи за сутки, за 2 часа и '
            f'за 5 минут, нажав на кнопку:\n"♻️ Стандартные уведомления". \n\nМожете каждое уведомление в '
            'отдельности изменить, добавить свой текст, ссылки с материалами или что-то ещё, и задать своё '
            f'время, за сколько до мероприятия оповестить пользователей. Для этого нажмите на кнопку:\n"⚙ Настроить '
            f'уведомления" затем выберите период за сколько до события сделать рассылку и введите количество этих '
            'периодов\n\n❗️❗️❗️ Важно знать, уведомления будут получать только те пользователи вашей базы, кто '
            'записался на мероприятие. Чтобы оповестить всех пользователей, воспользуйтесь функционалом рассылки.'
            f'\n\n<u>Если Вы сейчас ничего не выберите - уведомления приходить не будут!</u>')



class AddEvent(StatesGroup):
    title = State()
    description = State()
    date = State()
        
    
class EditEventTitle(StatesGroup):
    event = State()
    title = State()
    
    
class EditEventDescription(StatesGroup):
    event = State()
    description = State()
    
    
class EditEventDate(StatesGroup):
    event = State()
    date = State()
    
    
class EventReminder(StatesGroup):
    event = State()
    reminder_num = State()
    time = State()
    message = State()
    

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
        date = datetime.strptime(message.text, f'%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer(
            f'Неверный формат даты и времени. Пожалуйста, введите дату и время события в формате\nДД.ММ.ГГГГ ЧЧ:ММ')
        return
    if date < datetime.now() + timedelta(days=1):
        await message.answer('Дата события должна быть минимум на 24 часа позже настоящего времени!')
        return
    await state.update_data(date=date)
    data = await state.get_data()
    await set_event(data)
    await state.clear()
    event_id = await get_max_event_id()
    await message.answer('Мероприятие успешно добавлено. Хотите ли пригласить на него Ваших подписчиков?',
                         reply_markup=await inline.suggest_invite(event_id))

@router.callback_query(IsAdmin(), F.data.startswith('send_invitations_'))
async def send_invitations(callback: CallbackQuery, bot: Bot):
    event_id = callback.data.split('_')[2]
    event = await get_event_by_id(event_id)
    await callback.message.edit_text('Подождите... идёт рассылка🔊.')
    max_id = await get_max_user_id()
    message = f'<b>{event.title}</b>\n\n{event.description}\n\n<b>{event.date}</b>'
    fail = 0
    for user in await get_users():
        try:
            await bot.send_message(chat_id=user.tg_id, text=message, reply_markup=await inline.enroll_user(event_id))
        except:
            fail += 1
            pass
    success = max_id - fail
    await callback.message.answer(
        f'🎉 Рассылка успешно завершена!\n✅ Доставлено пользователям: <b>{success}</b> \n'
        f'⛔️ Не доставлено, отключили бота: <b>{fail}</b>')
    await callback.message.answer(reminder_hint, reply_markup=await inline.choose_reminders(event_id))
    
@router.callback_query(IsAdmin(), F.data.startswith('choose_reminders_'))
async def choose_reminders(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    await callback.message.edit_text(reminder_hint, reply_markup=await inline.choose_reminders(event_id))

@router.callback_query(IsAdmin(), F.data.startswith('base_reminders_'))
async def base_reminders(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    await schedule_base_event_reminders(event_id)
    await callback.message.edit_text('Стандартные уведомления успешно установлены!', reply_markup=reply.admin_main)
    
@router.callback_query(IsAdmin(), F.data.startswith('custom_reminders_'))
async def custom_reminders(callback: CallbackQuery):   
    event_id = callback.data.split('_')[2]
    await callback.message.edit_text(f'Выберите период для отправки уведомления:',
                                reply_markup=await inline.event_reminders_kb(event_id))
 
@router.callback_query(IsAdmin(), F.data.startswith("edit_reminders_")) 
async def edit_reminders(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    await set_base_reminders(event_id)
    await callback.message.edit_text(f'Выберите период для отправки уведомления:',
                                reply_markup=await inline.event_reminders_kb(event_id))
    
@router.callback_query(IsAdmin(), F.data.startswith("set_reminder_"))
async def set_reminder(callback: CallbackQuery, state: FSMContext):
    reminder_num = int(callback.data.split('_')[2])
    event_id = callback.data.split('_')[3]
    await set_base_reminders(event_id)
    await state.update_data(event=event_id, reminder_num=reminder_num)
    term = ''
    if reminder_num == 1:
        term = 'дней'
    if reminder_num == 2:
        term = 'часов'
    if reminder_num == 3:
        term = 'минут'
    await callback.message.edit_text(f'Введите за сколько {term} до события я отправлю участникам уведомление',
                                     reply_markup=inline.cancel_action)
    await state.set_state(EventReminder.time)
    
@router.message(IsAdmin(), EventReminder.time)
async def set_reminder_time(message: Message, state: FSMContext):
    try:
        time = int(message.text)
    except ValueError:
        await message.answer('Неверный формат времени. Пожалуйста, введите число')
        return
    if time < 1:
        await message.answer('Время должно быть больше нуля')
        return
    data = await state.get_data()
    event_id = data['event']
    reminder_num = data['reminder_num']
    reminder_time = None
    event = await get_event_by_id(event_id)
    if reminder_num == 1:
        if event.date - timedelta(days=time) < datetime.now():
            await message.answer('Похоже, что Вы поставили уведомление раньше настоящего времени. Попробуйте ещё раз')
            return
        reminder_time = event.date - timedelta(days=time)
    if reminder_num == 2:
        reminder_time = event.date - timedelta(hours=time)
    if reminder_num == 3:
        reminder_time = event.date - timedelta(minutes=time)
    await state.update_data(time=reminder_time)
    await state.set_state(EventReminder.message)
    await message.answer('Теперь введите сообщениe, которое получат участники мероприятия в указанный срок')
    
@router.message(IsAdmin(), EventReminder.message)
async def set_reminder_message(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    data = await state.get_data()
    await set_custom_reminder(data)
    await state.clear()
    event_id = data['event']
    await schedule_custom_reminder(event_id)
    await message.answer('Уведомление успешно изменено. Изменить другое?', 
                         reply_markup=await inline.event_reminders_kb(event_id))
    
@router.callback_query(IsAdmin(), F.data.startswith("predelete_event_"))
async def predelete_event_selected(callback: CallbackQuery):
    event_id = callback.data.split('_')[2]
    warning = ('Подтверждаете удаление мероприятия вместе со списком участников и Вашими напоминаниями? '
    'Вы можете просто изменить его')
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
    event_id = callback.data.split('_')[2]
    await callback.message.edit_text('Что именно вы бы хотели изменить?', reply_markup=await inline.edit_event(event_id))

@router.callback_query(IsAdmin(), F.data.startswith("edit_title_"))
async def edit_event_title(callback: CallbackQuery, state: FSMContext):
    await state.update_data(event=callback.data.split('_')[2])
    await state.set_state(EditEventTitle.title)
    await callback.message.edit_text(
        'Введите новое название события. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
        reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditEventTitle.title)
async def edit_event_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    data = await state.get_data()
    await state.clear()
    event_id = data['event']
    await edit_event(data)
    await message.answer('Название успешно изменено. Желаете редактировать что-нибудь ещё?', 
                         reply_markup=await inline.edit_event(event_id))
   
@router.callback_query(IsAdmin(), F.data.startswith("edit_description_"))
async def edit_event_title(callback: CallbackQuery, state: FSMContext):
    await state.update_data(event=callback.data.split('_')[2])   
    await state.set_state(EditEventDescription.description)
    await callback.message.edit_text('Введите новое описание события', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditEventDescription.description)
async def edit_event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()
    event_id = data['event']
    await edit_event(data)
    await message.answer('Описание успешно изменено. Желаете редактировать что-нибудь ещё?', 
                         reply_markup=await inline.edit_event(event_id))

@router.callback_query(IsAdmin(), F.data.startswith("edit_date_"))
async def edit_event_title(callback: CallbackQuery, state: FSMContext):
    await state.update_data(event=callback.data.split('_')[2])     
    await state.set_state(EditEventDate.date)
    await callback.message.edit_text(f"Введите новую дату события в формате\nДД.ММ.ГГГГ ЧЧ:ММ", 
                                     reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditEventDate.date)
async def edit_event_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, f'%d.%m.%Y %H:%M')
    except ValueError:
        await message.answer(
            f'Неверный формат даты и времени. Пожалуйста, введите дату и время события в формате\nДД.ММ.ГГГГ ЧЧ:ММ')
        return
    if date < datetime.now()  + timedelta(days=1):
        await message.answer('Дата события должна быть минимум на 24 часа позже настоящего времени')
        return
    await state.update_data(date=date)
    data = await state.get_data()
    event_id = data['event']
    await edit_event(data)
    await state.clear()
    reminders = await get_event_reminders(event_id)
    if reminders:
        await schedule_custom_reminder(event_id)
    else:
        await schedule_base_event_reminders(event_id)
    await message.answer('Дата мероприятия успешно изменена.  Желаете редактировать что-нибудь ещё?', 
                         reply_markup=await inline.edit_event(event_id))

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
            await callback.message.edit_text(message_text, reply_markup=inline.cancel_action)

async def send_admin_reminder(event_id):
    bot = Bot(token=TOKEN)
    bot.default.parse_mode = 'HTML'
    ADMIN_USER_IDS = await get_admins()
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
        with suppress(TelegramForbiddenError):
            await bot.send_message(chat_id=admin, text=message_text)
    await bot.session.close() 

async def send_base_participants_reminder(event_id):
    bot = Bot(token=TOKEN, parse_mode='HTML')
    event = await get_event_by_id(event_id)
    participants = await get_participants(event_id)
    admins = await get_admins()
    fail  = 0
    success = 0
    formatted_date = event.date.strftime(f'%d.%m.%Y в %H:%M')
    default_newsletter = ('Здравствуйте❗ Увлекательное путешествие в мир знаний уже на пороге❗ Скоро стартует '
        f'<b>{event.title}</b>, который расширит ваши горизонты и предоставит ценные инсайты👌. '
        f'Мы будем рады видеть вас <b>{formatted_date}</b>')
    for participant in participants:
        try:
            await bot.send_message(chat_id=participant.tg_id, text=default_newsletter)
            success += 1
        except TelegramForbiddenError:
            fail += 1
    with suppress(TelegramForbiddenError):
        for admin in admins:
            await bot.send_message(chat_id=admin, 
                text= f'🎉 Рассылка напоминания участникам о {event.title} успешно завершена!\n '
                f'✅ Доставлено пользователям: <b>{success}</b>\n⛔️ Не доставлено, отключили бота: <b>{fail}</b>')
    await bot.session.close()

async def schedule_base_event_reminders(event_id):
    event = await get_event_by_id(event_id)
    if event.date > datetime.now():
        events_scheduler.add_job(send_base_participants_reminder, 'date', 
                            run_date=event.date - timedelta(days=1), 
                            args=(event.id,), id=f'1_day_{event_id}', replace_existing=True)
        events_scheduler.add_job(send_base_participants_reminder, 'date',
                            run_date=event.date - timedelta(hours=2),
                            args=(event.id,), id=f'2_hours_{event_id}', replace_existing=True)
        events_scheduler.add_job(send_base_participants_reminder, 'date',
                            run_date=event.date - timedelta(minutes=5),
                            args=(event.id,), id=f'5_minutes_{event_id}', replace_existing=True)
        evening_reminder_trigger = CronTrigger(hour=19, minute=0, end_date=event.date, jitter=300)
        events_scheduler.add_job(send_admin_reminder, evening_reminder_trigger, args=(event.id,),
                                id=f'cron_event_{event_id}', replace_existing=True)
    
async def send_custom_participants_reminder(event_id, reminder_num):
    bot = Bot(token=TOKEN, parse_mode='HTML')
    event = await get_event_by_id(event_id)
    participants = await get_participants(event_id)
    admins = await get_admins()
    message = await get_reminder_message(event_id, reminder_num)
    success = 0
    fail = 0
    for participant in participants:
        try:
            await bot.send_message(chat_id=participant.tg_id, text=message)
            success += 1
        except TelegramForbiddenError:
            fail += 1
    with suppress(TelegramForbiddenError):
        for admin in admins:
            await bot.send_message(chat_id=admin, 
                text= f'🎉 Рассылка напоминания участникам о {event.title} успешно завершена!\n '
                f'✅ Доставлено пользователям: <b>{success}</b>\n⛔️ Не доставлено, отключили бота: <b>{fail}</b>')
    await bot.session.close()    
    
async def schedule_custom_reminder(event_id):
    event = await get_event_by_id(event_id)
    if event.date > datetime.now():
        reminders = await get_event_reminders(event_id)
        for reminder in reminders:
            events_scheduler.add_job(send_custom_participants_reminder, 'date',
                                run_date=reminder.time,
                                args=(event_id, reminder.reminder_num), 
                                id=f'reminder_{reminder.id}',
                                replace_existing=True)
        evening_reminder_trigger = CronTrigger(hour=19, minute=0, end_date=event.date)
        events_scheduler.add_job(send_admin_reminder, evening_reminder_trigger,
                                args=(event.id,), id=f'cron_event_{event_id}', replace_existing=True)
    
async def restart_event_reminders():
    events_scheduler.remove_all_jobs()
    upcoming_events = await get_events()
    for event in upcoming_events:
        reminders = await get_event_reminders(event.id)
        if reminders:
            await schedule_custom_reminder(event.id)
        else:
            await schedule_base_event_reminders(event.id)
