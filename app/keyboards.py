from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.database.requests import (get_contacts, get_services, get_cases, 
                                   get_events, get_services)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

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

new_contacts_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_contact'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_cases_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_case'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_services_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_service'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_events_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_event'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_briefing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать', callback_data='create_briefing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])


start_briefing_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать', callback_data='start_briefing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

in_briefing_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить', callback_data='next_question_'),
        InlineKeyboardButton(text='Изменить', callback_data='edit_answer_')],
            [InlineKeyboardButton(text='Начать заново', callback_data='start_briefing'),
            InlineKeyboardButton(text='Закончить', callback_data='end_briefing')]])  
    
confirm_delete_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Согласен', callback_data='confirmed_delete_contacts'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_delete')]])

participants_newsletter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сделать рассылку', callback_data='newsletter'),
     InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

cancel_action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

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
    events = await get_events()
    keyboard = InlineKeyboardBuilder()
    for event in events:
        keyboard.add(InlineKeyboardButton(text=event.title, callback_data=f'events_{event.id}'))
    return keyboard.adjust(1).as_markup()

async def admin_get_events_keyboard():
    events = await get_events()
    keyboard = InlineKeyboardBuilder()
    for event in events:
        keyboard.add(InlineKeyboardButton(text=event.title, callback_data=f'events_{event.id}'))
    keyboard.add(InlineKeyboardButton(text='Добавить мероприятие', callback_data='add_event'),
                 InlineKeyboardButton(text='Отмена', callback_data='cancel_action'))
    return keyboard.adjust(1).as_markup()

async def event_chosen_keyboard(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data=f'edit_event_{event_id}'),
    InlineKeyboardButton(text='Удалить', callback_data=f'delete_event_{event_id}')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action'),
     InlineKeyboardButton(text="Участники", callback_data=f'participants_{event_id}')]])
    return keyboard

async def enroll_user_keyboard(event_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Записаться', callback_data=f'enroll_user_{event_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


