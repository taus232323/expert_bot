from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


new_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Создать', callback_data='add_welcome'),
        InlineKeyboardButton(text='⏳ Позже', callback_data='cancel_action')]])

edit_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙ Изменить', callback_data='edit_welcome'),
        InlineKeyboardButton(text='❌ Удалить', callback_data='predelete_welcome')],
    [InlineKeyboardButton(text='🔙 На главную', callback_data='cancel_action')]])

confirm_delete_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтверждаю', callback_data='delete_welcome'),
        InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

contacts = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✍ Добавить', callback_data='add_contact'),
        InlineKeyboardButton(text='⚙ Изменить', callback_data='edit_contacts')],
            [InlineKeyboardButton(text='❌ Удалить', callback_data='predelete_contact'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

new_contact = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Добавить', callback_data='add_contact'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

confirm_delete_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтверждаю', callback_data='delete_contacts'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_delete')]])

new_case = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Добавить', callback_data='add_case'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

user_got_case = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❓ Заполнить бриф', callback_data='show_instruction')],
    [InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

new_service = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Добавить', callback_data='add_service'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

new_event = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Добавить', callback_data='add_event'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

new_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Добавить', callback_data='add_instruction'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

edit_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙ Изменить', callback_data='edit_instruction'),
            InlineKeyboardButton(text='❌ Удалить', callback_data='delete_instruction')],
    [InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

create_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Создать брифинг', callback_data='create_briefing')],
            [InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action'),
    InlineKeyboardButton(text='⚠ Инструкция', callback_data='instruction')]])

in_create_briefing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✍ Добавить', callback_data='add_question'),
        InlineKeyboardButton(text='👀 Посмотреть', callback_data='view_briefing')],
            [InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

admin_get_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙ Изменить', callback_data='edit_briefing'),
            InlineKeyboardButton(text='❌ Удалить', callback_data='predelete_briefing')],
    [InlineKeyboardButton(text='⚠ Инструкция', callback_data='instruction'),
    InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

edit_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍ Добавить', callback_data='add_question'),
    InlineKeyboardButton(text='⚙ Изменить', callback_data='edit_question')],
    [InlineKeyboardButton(text='❌ Удалить', callback_data='predelete_briefing'),
    InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])
     
confirm_delete_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтверждаю', callback_data='delete_briefing'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

start_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👉 Начать', callback_data='start_briefing'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

in_briefing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👉 Продолжить', callback_data='continue'),
        InlineKeyboardButton(text='⚙ Изменить', callback_data='edit_answer')],
            [InlineKeyboardButton(text='↩ Начать заново', callback_data='start_briefing'),
            InlineKeyboardButton(text='🛑 Закончить', callback_data='preend_briefing')]])  

end_briefing_selected = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='👉 Вернуться', callback_data='resume_briefing'),
            InlineKeyboardButton(text='⛔ Закончить', callback_data='end_briefing')]])
    
briefing_finished = InlineKeyboardMarkup(inline_keyboard=[
     [InlineKeyboardButton(text='🔄 Сначала', callback_data='restart_briefing'),
    InlineKeyboardButton(text='🔙 Меню', callback_data='to_main')]])

to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 На главную', callback_data='to_main')]])
    
cancel_action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])

admin_support = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💡 Предложить идею', callback_data='suggest_idea'),
        InlineKeyboardButton(text='🤬 Написать о проблеме', callback_data='report_problem')],
    [InlineKeyboardButton(text='🎁 Запросить промо', callback_data='ask_promo'),
        InlineKeyboardButton(text='💳 Оплатить подписку', callback_data='pay_subscription')]])

about_bot = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📃 Лицензионное соглашение', url='https://tmeet.ru/license_agreement_bot/')],
    [InlineKeyboardButton(text='📃 Обработка персональных данных', url='https://tmeet.ru/personal_data_bot/')],
    [InlineKeyboardButton(text='🔥 Заказать такого бота себе', url='https://tmeet.ru/personal_data_bot/')]])

async def go_to_support(client_link):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚡ Перейти', url=f'https://t.me/MstBiBot?start={client_link}')],
    [InlineKeyboardButton(text='▶ Добавить админа', callback_data='new_admin')]])
    return keyboard

async def case_chosen(case_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data=f'edit_case_{case_id}'),
    InlineKeyboardButton(text='❌Удалить', callback_data=f'delete_case_{case_id}')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])
    return keyboard

async def service_chosen(service_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data=f'edit_service_{service_id}'),
    InlineKeyboardButton(text='❌Удалить', callback_data=f'delete_service_{service_id}')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])
    return keyboard

async def order_service(service_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🤝 Заказать услугу', callback_data=f'order_service_{service_id}')],
    [InlineKeyboardButton(text='❓ Заполнить бриф', callback_data='show_instruction')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])
    return keyboard

async def event_chosen(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data=f'edit_event_{event_id}'),
    InlineKeyboardButton(text='❌Удалить', callback_data=f'predelete_event_{event_id}')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action'),
     InlineKeyboardButton(text="🚻Участники", callback_data=f'participants_{event_id}')],
    [InlineKeyboardButton(text='⏰ Напоминания участникам', callback_data=f'edit_reminders_{event_id}')]])
    return keyboard

async def event_reminders_kb(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1️⃣ Дни до ...', callback_data=f'set_reminder_1_{event_id}'),
    InlineKeyboardButton(text='2️⃣ Часы до ...', callback_data=f'set_reminder_2_{event_id}')],
    [InlineKeyboardButton(text='3️⃣ Минуты до ...', callback_data=f'set_reminder_3_{event_id}'),
    InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])
    return keyboard

async def suggest_invite(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Пригласить', callback_data=f'send_invitations_{event_id}')],
    [InlineKeyboardButton(text='⌛ Приглашу потом', callback_data=f'choose_reminders_{event_id}')]])
    return keyboard

async def choose_reminders(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='♻️ Cтандартные уведомления', callback_data=f'base_reminders_{event_id}')],
    [InlineKeyboardButton(text='⚙ Настроить уведомления', callback_data=f'custom_reminders_{event_id}')]])
    return keyboard
    
async def edit_event(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📘 Название', callback_data=f'edit_title_{event_id}'),
     InlineKeyboardButton(text='📖 Описание', callback_data=f'edit_description_{event_id}')],
    [InlineKeyboardButton(text='📅 Дата', callback_data=f'edit_date_{event_id}'),
    InlineKeyboardButton(text='⏰ Уведомления', callback_data=f'edit_reminders_{event_id}')]])
    return keyboard

async def confirm_delete_event(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтверждаю', callback_data=f'delete_event_{event_id}')],
            [InlineKeyboardButton(text='⚙ Изменить', callback_data=f'edit_event_{event_id}'),
            InlineKeyboardButton(text='⛔ Отмена', callback_data='cancel_action')]])
    return keyboard
     
async def enroll_user(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💾 Записаться', callback_data=f'enroll_user_{event_id}'),
    InlineKeyboardButton(text='⛔ Отмена', callback_data='to_main')]])
    return keyboard