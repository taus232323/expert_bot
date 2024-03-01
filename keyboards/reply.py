from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📖Контакты'), KeyboardButton(text='💎Кейсы')],
        [KeyboardButton(text='🗣Мероприятия'), KeyboardButton(text='👍Услуги')],
        [KeyboardButton(text='❓Брифинг')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

admin_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📖Контакты'), KeyboardButton(text='💎Кейсы')],
        [KeyboardButton(text='🗣Мероприятия'), KeyboardButton(text='👍Услуги')],
        [KeyboardButton(text='❓Брифинг'), KeyboardButton(text='👋Приветствие')],
        [KeyboardButton(text='✍Рассылка'), KeyboardButton(text='🛒Подписка')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)
