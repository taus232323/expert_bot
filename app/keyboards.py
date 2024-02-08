from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.database.requests import (get_contacts, get_briefing, get_services, get_cases, 
                                   get_events, get_service_by_id, get_services)
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
    return keyboard.adjust(1).as_markup()

async def admin_get_cases_keyboard():
    cases = await get_cases()
    keyboard = InlineKeyboardBuilder()
    for case in cases:
        keyboard.add(InlineKeyboardButton(text=case.title, callback_data=f'cases_{case.id}'))
    keyboard.add(InlineKeyboardButton(text='Добавить кейс', callback_data='add_case'))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_action'))
    return keyboard.adjust(1).as_markup()

async def case_chosen_keyboard(case_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data=f'edit_case_{case_id}'),
    InlineKeyboardButton(text='Удалить', callback_data=f'delete_case_{case_id}')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])
    return keyboard

async def get_services_keyboard():
    services = await get_services()
    keyboard = InlineKeyboardBuilder()
    for service in services:
        keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f'services_{service.id}'))
    return keyboard.adjust(1).as_markup()

async def admin_get_services_keyboard():
    services = await get_services()
    keyboard = InlineKeyboardBuilder()
    for service in services:
        keyboard.add(InlineKeyboardButton(text=service.title, callback_data=f'services_{service.id}'))
    keyboard.add(InlineKeyboardButton(text='Добавить услугу', callback_data='add_service'),
                 InlineKeyboardButton(text='Отмена', callback_data='cancel_action'))
    return keyboard.adjust(1).as_markup()

async def service_chosen_keyboard(service_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data=f'edit_service_{service_id}'),
    InlineKeyboardButton(text='Удалить', callback_data=f'delete_service_{service_id}')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])
    return keyboard
    








async def get_events_keyboard():
    events_kb = InlineKeyboardMarkup(row_width=2)
    events = await get_events()
    for event in events:
        events_kb.add(InlineKeyboardButton(text=events.name, callback_data=f'events_{events.id}'))
    return events_kb.adjust(2).as_markup()


async def get_briefing_keyboard():
    briefing_kb = InlineKeyboardMarkup(row_width=2)
    briefing_categories = await get_briefing()
    for briefing in briefing_categories:
        briefing_kb.add(InlineKeyboardButton(text=briefing.name, callback_data=f'briefing_{briefing.id}'))
    return briefing_kb.adjust(2).as_markup()

