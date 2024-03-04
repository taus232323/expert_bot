from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from settings import ADMIN_USER_IDS, TOKEN, SUPER_ADMIN_USER_IDS
from keyboards import reply, inline, builders 
from filters.is_admin import IsAdmin
from filters.is_superadmin import IsSuperAdmin
from data.requests import get_paid_days, update_paid_days

class SuggestIdea(StatesGroup):
    idea = State()
    seek_help = State()
    send_answer = State()


days_scheduler = AsyncIOScheduler()
router = Router()

support_hint = (
    "В этом меню вы можете задать любой вопрос касательно работы бота, написать предложение разработчикам "
            f"бота, запросить промо дни для изучение бота, и оплатить подписку.\n\nВся переписка будет отображаться "
            "у Вас в боте. Специалисты ответят Вам в кратчайшие сроки в рабочее время.")

@router.message(IsAdmin(), F.text.lower() == "🛠 поддержка")
async def support_selected(message: Message, bot: Bot):
    bot_me = await bot.get_me()
    paid_days = await get_paid_days()
    await message.answer(
        f"🛠 Добро пожаловать в меню поддержки.\nВам доступно дней активной подписки: <b>{paid_days}</b>\n")
    await message.answer(support_hint, reply_markup=await inline.go_to_support(bot_me.username))
   
async def change_paid_days(days: int):
    current_paid_days = await get_paid_days()
    if current_paid_days > 0:
        print('change')
        new_paid_days = current_paid_days + days
        await update_paid_days(new_paid_days)
        if not days_scheduler.get_job(change_paid_days):
            await schedule_decrease_paid_days()
    else:
        ADMIN_USER_IDS = ADMIN_USER_IDS[:1]
        await send_lease_reminder()

async def send_lease_reminder():
    bot = Bot(TOKEN)
    bot_me = await bot.get_me()
    for admin in ADMIN_USER_IDS:
        try:
            await bot.send_message(admin, 'Ваша подписка закончилась. Перейдите в бота оплаты для её продления',
                                   reply_markup=await inline.go_to_support(bot_me.username))
            days_scheduler.remove_job(change_paid_days)
        except:
            pass
    await bot.session.close()  
   
async def schedule_decrease_paid_days():
    days_scheduler.add_job(change_paid_days, CronTrigger(hour=21, minute=56), args=[-1])
    days_scheduler.start()
    print('start')
  
       
@router.callback_query(IsAdmin(), F.data == "suggest_idea")
async def suggest_idea(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Отправьте ваше предложение", reply_markup=inline.cancel_action)
    await state.set_state(SuggestIdea.idea)
      
@router.message(IsAdmin(), SuggestIdea.idea)
async def send_idea(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(idea=message.text)
    request_subject = f"Новое предложение от {message.from_user.username}\n\n{message.text}"
    for super_admin in SUPER_ADMIN_USER_IDS:
        await bot.send_message(super_admin, request_subject, reply_markup=inline.answer_idea)
    await state.set_state(SuggestIdea.seek_help)
    
@router.callback_query(IsSuperAdmin(), F.data == "answer_idea", SuggestIdea.seek_help)
async def answer_idea(callback: CallbackQuery, state: FSMContext):
    ...
   

