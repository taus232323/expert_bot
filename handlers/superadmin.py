from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.is_superadmin import IsSuperAdmin
from data.requests import get_users, set_admin, get_user_by_id
from keyboards import reply


class AddAdmin(StatesGroup):
    admin_id = State()


router = Router()

@router.message(IsSuperAdmin(), F.text.lower() == "▶ добавить админа")
async def add_admin_chosed(message: Message, state: FSMContext):
    users = await get_users()
    user_info = "\n".join([f"id:{user.id} @{user.username}" for user in users])
    await message.answer(user_info)
    await state.set_state(AddAdmin.admin_id)
    await message.answer('Введите ID пользователя которого хотите сделать администратором')

@router.message(IsSuperAdmin(), AddAdmin.admin_id)
async def add_new_admin(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        admin_id = int(message.text)
    else:
        await message.answer('Вы ввели не число')
        return
    user = await get_user_by_id(admin_id)
    await set_admin(user.tg_id)
    await message.answer(f'Администратор {user.username} добавлен')
    try:
        await bot.send_message(user.tg_id, 'Вы теперь администратор', reply_markup=reply.admin_main)
    except:
        await message.answer('Не удалось отправить сообщение администратору')

    
@router.message()
async def echo(message: Message):
    await message.answer("Я не понимаю, что вы хотите🤷‍♂️")
    
    

    

