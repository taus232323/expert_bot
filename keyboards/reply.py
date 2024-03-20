from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📖 Контакты'), KeyboardButton(text='💎 Кейсы')],
        [KeyboardButton(text='📆 Мероприятия'), KeyboardButton(text='🟢 Услуги')],
        [KeyboardButton(text='❓ Брифинг')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

admin_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👋 Приветствие'), KeyboardButton(text='📖 Контакты')],
        [KeyboardButton(text='🟢 Услуги'), KeyboardButton(text='💎 Кейсы')],
        [KeyboardButton(text='❓ Брифинг'), KeyboardButton(text='📆 Мероприятия')],
        [KeyboardButton(text='📣 Рассылка'), KeyboardButton(text='🛠 Поддержка')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

super_admin_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👋 Тг-визитка'), KeyboardButton(text='📖 Контакты')],
        [KeyboardButton(text='🟢 Услуги'), KeyboardButton(text='💎 Кейсы')],
        [KeyboardButton(text='❓ Брифинг'), KeyboardButton(text='📆 Мероприятия')],
        [KeyboardButton(text='📣 Рассылка'), KeyboardButton(text='▶ Добавить админа')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

leave_default = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='♻️ Cтандартные уведомления')],
        [KeyboardButton(text='⚙ Настроить уведомления')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите один из вариантов',
    one_time_keyboard=True
    )