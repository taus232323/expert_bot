from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.database.requests import get_contacts, get_briefing, get_services, get_cases, get_events, edit_contact, get_case_by_id
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

user_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Контакты'), KeyboardButton(text='Кейсы')],
        [KeyboardButton(text='Мероприятия'), KeyboardButton(text='Услуги')],
        [KeyboardButton(text='Пройти опрос')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True
)

contacts_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить', callback_data='add_contact'),
        InlineKeyboardButton(text='Изменить', callback_data='edit_contacts')],
            [InlineKeyboardButton(text='Удалить', callback_data='delete_contact'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

confirm_delete_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Согласен', callback_data='confirmed_delete_contacts'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_delete')]])

add_case_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_case'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

edit_cases_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_cases'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

async def edit_contact_kb():
    contacts = await get_contacts()
    keyboard = InlineKeyboardBuilder()
    for contact in contacts:
        keyboard.add(InlineKeyboardButton(text=contact.contact_type,
                                      callback_data=f'edit_contact_{contact.id}'))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_action'))
    return keyboard.adjust(2).as_markup()

async def get_cases_keyboard():
    cases = await get_cases()
    keyboard = InlineKeyboardBuilder()
    for case in cases:
        keyboard.add(InlineKeyboardButton(text=case.title, callback_data=f'cases_{case.id}'))
    return keyboard.adjust(2).as_markup()

async def case_keyboard(case_id):
    case = await get_case_by_id(case_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_action'))
    return keyboard.adjust(2).as_markup()









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

