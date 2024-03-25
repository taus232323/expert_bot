from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.exceptions import TelegramForbiddenError

from settings import TOKEN
from keyboards import inline, reply
from filters.is_admin import IsAdmin
from data.requests import get_paid_days, update_paid_days, get_admins_to_remind, get_users, get_user_by_id, set_admin


days_scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
router = Router()

support_hint = (
    "Здесь вы можете перейти в нашего бота для оплаты подписки, запроса промо-доступа, чтобы сообщить о проблеме, "
    "или отправить предложение по улучшению Вашего бота. Так же Вы можете самостоятельно добавить администратора "
    "к Вашему боту")

class AddAdmin(StatesGroup):
    admin_id = State()
    
    
@router.message(IsAdmin(), F.text.lower() == "🛠 поддержка")
async def support_selected(message: Message, bot: Bot):
    bot_me = await bot.get_me()
    paid_days = await get_paid_days()
    await message.answer(
        f"🛠 Добро пожаловать в меню поддержки.\nВам доступно дней активной подписки: <b>{paid_days}</b>\n")
    await message.answer(support_hint, reply_markup=await inline.go_to_support(bot_me.username))

@router.callback_query(IsAdmin(), F.data == "new_admin")
async def add_admin_chosed(callback: CallbackQuery, state: FSMContext):
    users = await get_users()
    user_info = "\n".join([f"id:{user.id} @{user.username}" for user in users])
    await callback.message.edit_text(user_info)
    await state.set_state(AddAdmin.admin_id)
    await callback.message.answer('Введите ID пользователя которого хотите сделать администратором')

@router.message(IsAdmin(), AddAdmin.admin_id)
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
  
async def change_paid_days(days: int):
    current_paid_days = await get_paid_days()
    if current_paid_days == 0 and days < 0:
        await send_lease_reminder()
        days_scheduler.remove_all_jobs()
    elif current_paid_days >= 0:
        new_paid_days = current_paid_days + int(days)
        await update_paid_days(new_paid_days)
        if not days_scheduler.running:
            await schedule_decrease_paid_days()

async def send_lease_reminder():
    bot = Bot(TOKEN)
    bot_me = await bot.get_me()
    ADMIN_USER_IDS = await get_admins_to_remind()
    for admin in ADMIN_USER_IDS:
        try:
            await bot.send_message(admin, 'Ваша подписка закончилась. Перейдите в бота оплаты для её продления',
                                   reply_markup=await inline.go_to_support(bot_me.username))
        except TelegramForbiddenError:
            print(f'Не удалось отправить сообщение админу {admin}')
    await bot.session.close()  
   
async def schedule_decrease_paid_days():
    days_scheduler.add_job(change_paid_days, CronTrigger(hour=17, minute=7), args=[-1])
  