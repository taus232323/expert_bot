from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📖 Контакты'), KeyboardButton(text='💎 Кейсы и отзывы')],
        [KeyboardButton(text='📆 Мероприятия'), KeyboardButton(text='🟢 Услуги и товары')],
        [KeyboardButton(text='❓ Заполнить бриф'), KeyboardButton(text='⚠ О боте')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

admin_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👋 Телеграм визитка'), KeyboardButton(text='📖 Контакты')],
        [KeyboardButton(text='🟢 Услуги и товары'), KeyboardButton(text='💎 Кейсы и отзывы')],
        [KeyboardButton(text='❓ Брифинг'), KeyboardButton(text='📆 Мероприятия')],
        [KeyboardButton(text='📣 Рассылка'), KeyboardButton(text='🛠 Поддержка')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

super_admin_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='👋 Телеграм визитка'), KeyboardButton(text='📖 Контакты')],
        [KeyboardButton(text='🟢 Услуги и товары'), KeyboardButton(text='💎 Кейсы и отзывы')],
        [KeyboardButton(text='❓ Брифинг'), KeyboardButton(text='📆 Мероприятия')],
        [KeyboardButton(text='📣 Рассылка'), KeyboardButton(text='▶ Добавить админа')]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие',
    one_time_keyboard=True)

