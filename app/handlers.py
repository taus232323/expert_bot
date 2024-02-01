from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from settings import ADMIN_USER_IDS
import app.keyboards as kb
from app.database.requests import get_contacts


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer(f"Добро пожаловать, администратор {message.from_user.first_name}!"
                             "Выберите вариант из меню ниже", reply_markup = kb.admin_main)
    else:
        await message.answer(f"Добро пожаловать, {message.from_user.first_name}! "
                         "Выберите вариант из меню ниже", reply_markup = kb.user_main)
    
@router.message(F.text == "Контакты")
async def contact_selected(message: Message):
    contacts = await get_contacts()
    print(len(contacts))
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer(f"{message.from_user.first_name}, для добавления/изменения "
                                      "контактной информации следуйте инструкциям", reply_markup=kb.admin_keyboard)
    else:    
        if contacts:
            contact_info = "\n".join([f"{contact.contact_type}: {contact.phone}, {contact.email}, {contact.address}, {contact.working_hours}, {contact.office_address}" for contact in contacts])
            await message.answer(f"Моя контактная информация и график работы:\n{contact_info}")
        else:
            await message.answer("Контактная информация отсутствует.")
    
@router.callback_query(F.data.startswith("events_"))
async def event_selected(callback: CallbackQuery):
    events = await kb.get_events()
    events_list = "\n".join([f"{event.name} - {event.date}" for event in events])
    await callback.message.answer(f"Список мероприятий:\n{events_list}")
    await callback.answer()

@router.callback_query(F.data.startswith("event_detail_"))
async def event_detail_selected(callback: CallbackQuery):
    event_id = callback.data.split("_")[2]
    event = await kb.get_event(event_id)
    text = f"<b>{event.name}</b>\n\n{event.description}\n\nДата проведения: {event.date}"
    if event.image_url:
        await callback.message.answer_photo(photo=event.image_url, caption=text, parse_mode='HTML')
    else:
        await callback.message.answer(text, parse_mode='HTML')
    await callback.answer()

@router.callback_query(F.data.startswith("services_"))
async def services_selected(callback: CallbackQuery):
    services = await kb.get_services()
    services_list = "\n".join([f"{service.name}" for service in services])
    await callback.message.answer(f"Мои услуги:\n{services_list}")
    await callback.answer()

@router.callback_query(F.data.startswith("service_detail_"))
async def service_detail_selected(callback: CallbackQuery):
    service_id = callback.data.split("_")[2]
    service = await kb.get_service(service_id)
    text = f"<b>{service.name}</b>"
    if service.description:
        text += f"\n\n{service.description}"
    if service.image_url:
        await callback.message.answer_photo(photo=service.image_url, caption=text, parse_mode='HTML')
    else:
        await callback.message.answer(text, parse_mode='HTML')
    await callback.answer()

@router.callback_query(F.data.startswith("cases_"))
async def cases_selected(callback: CallbackQuery):
    cases = await kb.get_cases()
    cases_list = "\n".join([f"{case.name}" for case in cases])
    await callback.message.answer(f"Мои кейсы:\n{cases_list}")
    await callback.answer()
    
@router.callback_query(F.data.startswith("case_detail_"))
async def case_detail_selected(callback: CallbackQuery):
    case_id = callback.data.split("_")[2]
    case = await kb.get_case(case_id)
    text = f"<b>{case.name}</b>"
    if case.description:
        text += f"\n\n{case.description}"
    if case.image_url:
        await callback.message.answer_photo(photo=case.image_url, caption=text, parse_mode='HTML')
    else:
        await callback.message.answer(text, parse_mode='HTML')
    await callback.answer()

@router.callback_query(F.data.startswith("briefing_"))
async def briefing_selected(callback: CallbackQuery):
    await callback.message.answer(f"Брифинг", reply_markup=await kb.get_briefing_keyboard())
    await callback.answer()

@router.message()
async def echo(message: Message):
    await message.answer(f"Я не понимаю, что вы хотите")