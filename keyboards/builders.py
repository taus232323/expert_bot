from data.requests import (get_contacts, get_services, get_cases, get_answer_by_id, 
                                   get_events, get_services)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import  InlineKeyboardButton

async def edit_contact():
    contacts = await get_contacts()
    keyboard = InlineKeyboardBuilder()
    for contact in contacts:
        keyboard.button(text=contact.contact_type, callback_data=f'edit_contact_{contact.id}')
    keyboard.button(text='⛔Отмена', callback_data='cancel_action')
    return keyboard.adjust(2).as_markup()

async def get_cases_kb():
    cases = await get_cases()
    keyboard = InlineKeyboardBuilder()
    for case in cases:
        keyboard.button(text=f"💎{case.title}", callback_data=f'cases_{case.id}')
    return keyboard.adjust(1).as_markup()

async def admin_get_cases():
    cases = await get_cases()
    keyboard = InlineKeyboardBuilder()
    i = 0
    for case in cases:
        keyboard.button(text=f"💎{case.title}", callback_data=f'cases_{case.id}')
        i += 1
    keyboard.button(text='✍Добавить кейс', callback_data='add_case')
    keyboard.button(text='⛔Отмена', callback_data='cancel_action')
    return keyboard.adjust(*[1] * i, 2).as_markup()

async def get_services_kb():
    services = await get_services()
    keyboard = InlineKeyboardBuilder()
    for service in services:
        keyboard.button(text=f"👍{service.title}", callback_data=f'services_{service.id}')
    return keyboard.adjust(1).as_markup()

async def admin_get_services():
    services = await get_services()
    keyboard = InlineKeyboardBuilder()
    i = 0
    for service in services:
        keyboard.button(text=f"👍{service.title}", callback_data=f'services_{service.id}')
        i += 1
    keyboard.add(InlineKeyboardButton(text='✍Добавить услугу', callback_data='add_service'),
                 InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action'))
    return keyboard.adjust(*[1] * i, 2).as_markup()

async def get_events_kb():
    events = await get_events()
    keyboard = InlineKeyboardBuilder()
    for event in events:
        keyboard.button(text=f"👏{event.title}", callback_data=f'events_{event.id}')
    return keyboard.adjust(1).as_markup()

async def admin_get_events():
    events = await get_events()
    keyboard = InlineKeyboardBuilder()
    i = 0
    for event in events:
        keyboard.button(text=f"👏{event.title}", callback_data=f'events_{event.id}')
        i += 1
    keyboard.button(text='✍Добавить мероприятие', callback_data='add_event')
    keyboard.button(text='⛔Отмена', callback_data='cancel_action')
    return keyboard.adjust(*[1] * i, 2).as_markup()

async def generate_answer(line):
    answers = await get_answer_by_id(line)
    if ";" in answers:
        buttons = [button.strip() for button in answers.split(';')]
        keyboard = ReplyKeyboardBuilder()
        for answer in buttons:
            keyboard.button(text=answer)
        return keyboard.adjust(1).as_markup(resize_keyboard=True, one_time_keyboard=True,
                                            input_field_placeholder="Выберите ответ")
    else:
        return None