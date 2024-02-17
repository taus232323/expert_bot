from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from app.database.requests import (get_contacts, get_services, get_cases, 
                                   get_events, get_services)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


user_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Контакты'), KeyboardButton(text='Кейсы')],
        [KeyboardButton(text='Мероприятия'), KeyboardButton(text='Услуги')],
        [KeyboardButton(text='Пройти опрос')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

admin_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Контакты'), KeyboardButton(text='Кейсы')],
        [KeyboardButton(text='Мероприятия'), KeyboardButton(text='Услуги')],
        [KeyboardButton(text='Пройти опрос'), KeyboardButton(text='Приветствие')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

new_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать', callback_data='add_welcome'),
        InlineKeyboardButton(text='Позже', callback_data='cancel_action')]])

edit_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_welcome'),
        InlineKeyboardButton(text='Удалить', callback_data='predelete_welcome')],
    [InlineKeyboardButton(text='На главную', callback_data='cancel_action')]])

confirm_delete_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Уверен', callback_data='delete_welcome'),
        InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

contacts = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить', callback_data='add_contact'),
        InlineKeyboardButton(text='Изменить', callback_data='edit_contacts')],
            [InlineKeyboardButton(text='Удалить', callback_data='predelete_contact'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_contact'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

confirm_delete_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Согласен', callback_data='delete_contacts'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_delete')]])

new_cases = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_case'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_services = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_service'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_events = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_event'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

new_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_instruction'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

edit_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_instruction'),
            InlineKeyboardButton(text='Удалить', callback_data='delete_instruction')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

create_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создать', callback_data='create_briefing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')],
    [InlineKeyboardButton(text='Добавить инструкцию', callback_data='add_instruction')]])

in_create_briefing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить', callback_data='add_question'),
        InlineKeyboardButton(text='Посмотреть', callback_data='briefing')],
            [InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

admin_get_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data='edit_briefing'),
            InlineKeyboardButton(text='Удалить', callback_data='predelete_briefing')],
    [InlineKeyboardButton(text='Инструкция', callback_data='instruction'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

edit_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_question'),
    InlineKeyboardButton(text='Изменить', callback_data='edit_question')],
    [InlineKeyboardButton(text='Удалить', callback_data='predelete_briefing'),
    InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])
     
confirm_delete_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Согласен', callback_data='delete_briefing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

start_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать', callback_data='start_briefing'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])

in_briefing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Продолжить', callback_data='continue'),
        InlineKeyboardButton(text='Изменить', callback_data='edit_answer')],
            [InlineKeyboardButton(text='Начать заново', callback_data='start_briefing'),
            InlineKeyboardButton(text='Закончить', callback_data='preend_briefing')]])  

end_briefing_selected = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='Вернуться', callback_data='resume_briefing'),
            InlineKeyboardButton(text='Закончить', callback_data='end_briefing')]])
    
briefing_finished = InlineKeyboardMarkup(inline_keyboard=[
     [InlineKeyboardButton(text='Сначала', callback_data='restart_briefing'),
    InlineKeyboardButton(text='Меню', callback_data='to_main')]])
    
    
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

async def get_cases_kb():
    cases = await get_cases()
    keyboard = InlineKeyboardBuilder()
    for case in cases:
        keyboard.add(InlineKeyboardButton(text=case.title, callback_data=f'cases_{case.id}'))
    return keyboard.adjust(1).as_markup()


async def admin_get_cases_kb():
    cases = await get_cases()
    keyboard = InlineKeyboardBuilder()
    for case in cases:
        keyboard.add(InlineKeyboardButton(text=case.title, callback_data=f'cases_{case.id}'))
    keyboard.add(InlineKeyboardButton(text='Добавить кейс', callback_data='add_case'))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_action'))
    return keyboard.adjust(1).as_markup()

async def case_chosen_kb(case_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data=f'edit_case_{case_id}'),
    InlineKeyboardButton(text='Удалить', callback_data=f'delete_case_{case_id}')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])
    return keyboard

async def get_services_kb():
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
    InlineKeyboardButton(text='Удалить', callback_data=f'predelete_event_{event_id}')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_action'),
     InlineKeyboardButton(text="Участники", callback_data=f'participants_{event_id}')]])
    return keyboard

async def confirm_delete_event(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтверждаю', callback_data=f'delete_event_{event_id}')],
            [InlineKeyboardButton(text='Изменить', callback_data=f'edit_event_{event_id}'),
            InlineKeyboardButton(text='Отмена', callback_data='cancel_action')]])
    return keyboard
     

async def enroll_user_keyboard(event_id):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Записаться', callback_data=f'enroll_user_{event_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

def generate_answer(answers):
    if len(answers) > 1:
        answers = answers.split(";")
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for answer in answers:
            markup.add(KeyboardButton(answer))
    else:
        markup = None
    return markup


