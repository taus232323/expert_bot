from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from settings import ADMIN_USER_IDS
import app.keyboards as kb
from app.database.requests import (get_contacts, set_user, get_cases, get_case_by_id, get_services, get_service_by_id,
                                   get_events, get_event_by_id, set_participant)


router = Router()

@router.message(CommandStart())

async def cmd_start(message: Message):
    if isinstance(message, Message):
        await set_user(message.from_user.id, message.from_user.username)
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer(f"Добро пожаловать, администратор {message.from_user.first_name}!"
                             "нажмите на /apanel для доступа к админ-панели", reply_markup=kb.user_main)
    else:
        await message.answer(f"Добро пожаловать, {message.from_user.first_name}! "
                         "Выберите вариант из меню ниже", reply_markup=kb.user_main)

@router.callback_query(F.data == "to_main")        
async def to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Выберите вариант из меню ниже", reply_markup=kb.user_main)

    
@router.message(F.text == "Контакты")
async def contact_selected(message: Message):
    contacts = await get_contacts()   
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    if len(contact_info) < 2:
        await message.answer("Контактная информация отсутствует")
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите желаемую опцию:", reply_markup=kb.new_contacts_kb)
    else:
        await message.answer(f"Моя контактная информация и график работы:\n{contact_info}")
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите желаемую опцию:", reply_markup=kb.contacts_kb)
   
    
@router.message(F.text == "Кейсы")
async def cases_selected(message: Message):
    cases = await get_cases()
    cases_list = "\n".join([f"{case.title}" for case in cases])
    if len(cases_list) < 2:
        await message.answer("Кейсы отсутствуют")
    else:
        await message.answer("Мои самые лучшие кейсы:", reply_markup=await kb.get_cases_keyboard())
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer("Выберите кейс для изменения/удаления или добавьте новый", 
                             reply_markup=await kb.admin_get_cases_keyboard())
    
@router.callback_query(F.data.startswith("cases_"))    
async def case_detail_selected(callback: CallbackQuery):
    case = await get_case_by_id(callback.data.split("_")[1])
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(f"<b>{case.title}</b>\n\n{case.description}", 
                                         reply_markup=await kb.case_chosen_keyboard(case.id))
    else:
        await callback.message.edit_text(f"<b>{case.title}</b>\n\n{case.description}")
        
@router.message(F.text == "Услуги")
async def service_selected(message: Message):
    services  = await get_services()
    services_list = "\n".join([f"{service.title}" for service in services])
    if len(services_list) < 2:
        await message.answer("Услуги отсутствуют")
    else:
        await message.answer("Мои самые выгодные услуги:", reply_markup=await kb.get_services_keyboard())
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer("Выберите услугу для изменения/удаления или добавьте новую",
                             reply_markup=await kb.admin_get_services_keyboard())
        
@router.callback_query(F.data.startswith("services_"))
async def service_detail_selected(callback: CallbackQuery):
    service = await get_service_by_id(callback.data.split("_")[1])
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(f"<b>{service.title}</b>\n\n{service.description}", 
                                         reply_markup=await kb.service_chosen_keyboard(service.id))
    else:
        await callback.message.edit_text(f"<b>{service.title}</b>\n\n{service.description}")
               
@router.message(F.text == "Мероприятия")
async def event_selected(message: Message):
    events = await get_events()
    events_list = "\n".join([f"{event.title}" for event in events])
    if len(events_list) < 2:
        await message.answer("Мероприятия отсутствуют")
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer("Выберите мероприятие для изменения/удаления или добавьте новое",
                             reply_markup=await kb.admin_get_events_keyboard())
    else:
        await message.answer("Мои самые интересные мероприятия:", reply_markup=await kb.get_events_keyboard())

@router.callback_query(F.data.startswith("events_"))
async def event_detail_selected(callback: CallbackQuery):
    event = await get_event_by_id(callback.data.split("_")[1])
    formatted_date = event.date.strftime('%Y-%m-%d %H:%M')
    event_for_send = f"<b>{event.title}</b>\n\n{event.description}\n\n<b>{formatted_date}</b>"
    user = callback.from_user
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(event_for_send, reply_markup=await kb.event_chosen_keyboard(event.id))
    else:
        await callback.message.edit_text(event_for_send, reply_markup=await kb.enroll_user_keyboard(event.id))

@router.callback_query(F.data.startswith("enroll_"))
async def enroll_user(callback: CallbackQuery):
    event = await get_event_by_id(callback.data.split("_")[2])
    await callback.message.delete()
    if await set_participant(tg_id=callback.from_user.id, event_id=callback.data.split("_")[2]):
        await callback.message.answer(f"Вы успешно записаны на: <b>{event.title}</b>.\n"
                                    f"Дата и время события: <b>{event.date}</b>")
        await callback.message.answer("Я напомню Вам заранее, чтобы Вы не пропустили самое интересное. "
                                        "А пока что можете выбрать вариант из меню ниже", reply_markup=kb.user_main)
    else:
        await callback.message.answer(f"Вы уже записаны на: <b>{event.title}</b>.\n"
                                    f"Дата и время события: <b>{event.date}</b>")
        await callback.message.answer("Я напомню Вам заранее, чтобы Вы не пропустили самое интересное. "
                                        "А пока что можете выбрать вариант из меню ниже", reply_markup=kb.user_main)
        

@router.message()
async def echo(message: Message):
    await message.answer(f"Я не понимаю, что вы хотите")