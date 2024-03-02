from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import inline
from filters.is_admin import IsAdmin
from data.requests import get_max_user_id, get_users


admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"
router = Router()

class Newsletter(StatesGroup):
    message = State()
    

@router.message(IsAdmin(), F.text.lower() == '✍рассылка')
async def newsletter(message: Message, state: FSMContext):
    max_id = await get_max_user_id()
    await state.set_state(Newsletter.message)
    with open('handlers/admin/newsletter_hint.txt', 'r', encoding='utf-8') as text:
        newsletter_hint = text.read()
    await message.answer(newsletter_hint)
    await message.answer(
        f'Сейчас пользователей в Вашей базе: <b>{max_id}</b>\nОтправьте сообщение, которое вы хотите им разослать', 
                         reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка🔊.')
    max_id = await get_max_user_id()
    fail = 0
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            fail += 1
            pass
    success = max_id - fail
    await message.answer(
        f'🎉 Рассылке успешна завершена!\n✅ Доставлено <b>{success}</b> пользователям\n'
        f'⛔️ Не доставлено <b>{fail}</b> пользователям')
    await state.clear()