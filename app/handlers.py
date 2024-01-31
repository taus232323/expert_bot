from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from settings import USER_IDS
import app.keyboards as kb
from app.database.requests import get_events, get_briefing, get_cases, get_contacts, get_services

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}! "
                         "Выберите вариант из меню ниже", reply_markup = kb.user_keyboard)
   
    
@router.callback_query(F.data.startswith("contacts_"))
async def contact_selected(callback: CallbackQuery):
    await callback.message.answer("Моя контактная информация и график работы:",
                                  reply_markup=await kb.get_contacts_keyboard())
    await callback.answer()
    
    
@router.callback_query(F.data.startswith("events_"))
async def event_selected(callback: CallbackQuery):
    event_id = callback.data.split("_")[1]
    events = await kb.get_event(event_id)
    await callback.message.answer(f"<b>{events.name}</b>\n\n{events.description}\n\nДата проведения: {events.date}")
    await callback.answer()


@router.callback_query(F.data.startswith("briefing_"))
async def briefing_selected(callback: CallbackQuery):
    await callback.message.answer(f"Брифинг", reply_markup=await kb.get_briefing_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("services_"))
async def service_selected(callback: CallbackQuery):
    service_id = callback.data.split("_")[1]
    service = await kb.get_service(service_id)
    await callback.message.answer(f" Мои услуги", reply_markup=await kb.get_services_keyboard())
    await callback.message.answer(f"<b>{service.name}</b>\n\n{service.description}")
    await callback.answer()


@router.message()
async def echo(message: Message):
    await message.answer(f"Я не понимаю, что вы хотите")