from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, 
from app.database.requests import get_links, get_contacts
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from unicodedata import category


admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Кейсы')],
    [KeyboardButton(text='Контакты')],
    [KeyboardButton(text='Мероприятия')],
    [KeyboardButton(text='Услуги')],
    [KeyboardButton(text='Пройти опрос')],
    [KeyboardButton(text='Админ-панель')]
], resize_keyboard=True, input_field_placeholder='Выберите действие', one_time_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить')],
    [KeyboardButton(text='Изменить')],
    [KeyboardButton(text='Сделать рассылку')],
],    resize_keyboard=True, input_field_placeholder='Выберите действие', one_time_keyboard=True)

async def get_contacts_keyboard():
    contacts_kb = InlineKeyboardMarkup(row_width=2)
    contacts = await get_contacts()
    for contact in contacts:
        contacts_kb.add(InlineKeyboardButton(text=contacts.contact_type, callback_data=f'contacts_'))
    return contacts_kb.adjust(2).as_markup()