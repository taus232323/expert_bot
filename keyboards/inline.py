from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


new_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Создать', callback_data='add_welcome'),
        InlineKeyboardButton(text='⏳Позже', callback_data='cancel_action')]])

edit_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data='edit_welcome'),
        InlineKeyboardButton(text='❌Удалить', callback_data='predelete_welcome')],
    [InlineKeyboardButton(text='🔙На главную', callback_data='cancel_action')]])

confirm_delete_welcome = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Уверен', callback_data='delete_welcome'),
        InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

contacts = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✍Добавить', callback_data='add_contact'),
        InlineKeyboardButton(text='⚙Изменить', callback_data='edit_contacts')],
            [InlineKeyboardButton(text='❌Удалить', callback_data='predelete_contact'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

new_contact = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Добавить', callback_data='add_contact'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

confirm_delete_contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Согласен', callback_data='delete_contacts'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_delete')]])

new_case = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Добавить', callback_data='add_case'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

new_service = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Добавить', callback_data='add_service'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

new_event = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Добавить', callback_data='add_event'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

new_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Добавить', callback_data='add_instruction'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

edit_instruction = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data='edit_instruction'),
            InlineKeyboardButton(text='Удалить', callback_data='delete_instruction')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

create_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Создать', callback_data='create_briefing'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')],
    [InlineKeyboardButton(text='⚠Инструкция', callback_data='instruction')]])

in_create_briefing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✍Добавить', callback_data='add_question'),
        InlineKeyboardButton(text='👀Посмотреть', callback_data='view_briefing')],
            [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

admin_get_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data='edit_briefing'),
            InlineKeyboardButton(text='❌Удалить', callback_data='predelete_briefing')],
    [InlineKeyboardButton(text='⚠Инструкция', callback_data='instruction'),
    InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

edit_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Добавить', callback_data='add_question'),
    InlineKeyboardButton(text='⚙Изменить', callback_data='edit_question')],
    [InlineKeyboardButton(text='❌Удалить', callback_data='predelete_briefing'),
    InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])
     
confirm_delete_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Согласен', callback_data='delete_briefing'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

start_briefing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👉Начать', callback_data='start_briefing'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

in_briefing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='👉Продолжить', callback_data='continue'),
        InlineKeyboardButton(text='⚙Изменить', callback_data='edit_answer')],
            [InlineKeyboardButton(text='↩Начать заново', callback_data='start_briefing'),
            InlineKeyboardButton(text='🛑Закончить', callback_data='preend_briefing')]])  

end_briefing_selected = InlineKeyboardMarkup(inline_keyboard=[
 [InlineKeyboardButton(text='👉Вернуться', callback_data='resume_briefing'),
            InlineKeyboardButton(text='⛔Закончить', callback_data='end_briefing')]])
    
briefing_finished = InlineKeyboardMarkup(inline_keyboard=[
     [InlineKeyboardButton(text='🔄Сначала', callback_data='restart_briefing'),
    InlineKeyboardButton(text='🔙Меню', callback_data='to_main')]])
    
    
participants_newsletter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✍Сделать рассылку', callback_data='newsletter'),
     InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

cancel_action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])

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
    [InlineKeyboardButton(text='🤝Заказать', callback_data=f'order_service_{service_id}')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])
    return keyboard

async def event_chosen(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⚙Изменить', callback_data=f'edit_event_{event_id}'),
    InlineKeyboardButton(text='❌Удалить', callback_data=f'predelete_event_{event_id}')],
    [InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action'),
     InlineKeyboardButton(text="🚻Участники", callback_data=f'participants_{event_id}')]])
    return keyboard

async def confirm_delete_event(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅Подтверждаю', callback_data=f'delete_event_{event_id}')],
            [InlineKeyboardButton(text='⚙Изменить', callback_data=f'edit_event_{event_id}'),
            InlineKeyboardButton(text='⛔Отмена', callback_data='cancel_action')]])
    return keyboard
     
async def enroll_user(event_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💾Записаться', callback_data=f'enroll_user_{event_id}'),
    InlineKeyboardButton(text='🔙Назад', callback_data='to_main')]])
    return keyboard