from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.database.requests import get_links, get_contacts, get_briefing, get_services, get_cases, get_events
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

user_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Контакты'), KeyboardButton(text='Кейсы')],
        [KeyboardButton(text='Мероприятия'), KeyboardButton(text='Услуги')],
        [KeyboardButton(text='Пройти опрос')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True
)

async def get_contacts_keyboard():
    contacts_kb = InlineKeyboardMarkup(row_width=2)
    contacts = await get_contacts()
    for contact in contacts:
        contacts_kb.add(InlineKeyboardButton(text=contacts.contact_type, callback_data=f'contacts_'))
    return contacts_kb.adjust(2).as_markup()

async def get_events_keyboard():
    events_kb = InlineKeyboardMarkup(row_width=2)
    events = await get_events()
    for event in events:
        events_kb.add(InlineKeyboardButton(text=events.name, callback_data=f'events_{events.id}'))
    return events_kb.adjust(2).as_markup()

async def get_services_keyboard():
    services_kb = InlineKeyboardMarkup(row_width=2)
    services = await get_services()
    for service in services:
        services_kb.add(InlineKeyboardButton(text=service.name, callback_data=f'services_{services.id}'))
    return services_kb.adjust(2).as_markup()

async def get_briefing_keyboard():
    briefing_kb = InlineKeyboardMarkup(row_width=2)
    briefing_categories = await get_briefing()
    for briefing in briefing_categories:
        briefing_kb.add(InlineKeyboardButton(text=briefing.name, callback_data=f'briefing_{briefing.id}'))
    return briefing_kb.adjust(2).as_markup()

async def get_cases_keyboard():
    cases_kb = InlineKeyboardMarkup(row_width=2)
    cases = await get_cases()
    for case in cases:
        cases_kb.add(InlineKeyboardButton(text=cases.name, callback_data=f'casse_{cases.id}'))
    return cases_kb.adjust(2).as_markup()