from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram.exceptions import TelegramForbiddenError

from settings import ADMIN_USER_IDS, TOKEN, SUPER_ADMIN_USER_IDS
from app.admin import days_remaining

superadmin = Router()
scheduler = AsyncIOScheduler()
paid_days = 30

class UpRent(StatesGroup):
    rent_days = State()

@superadmin.message(IsSuperAdmin(), Command(commands=["rent"]))
async def rent(message: Message, state: FSMContext):
    await message.answer('На сколько дней продлить аренду этого бота?')
    await state.set_state(UpRent.rent_days)
    
@superadmin.message(IsSuperAdmin(), UpRent.rent_days)
async def update_rent(message: Message, state: FSMContext):
    if message.text.isdigit():
        days = int(message.text)
    else:
        await message.answer('Вы ввели не число')
        return
    days_remaining += days
    
    
@router.message()
async def echo(message: Message):
    await message.answer("Я не понимаю, что вы хотите🤷‍♂️")
    
    

    

