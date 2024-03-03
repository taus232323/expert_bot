from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.deep_linking import decode_payload, create_start_link

import settings
from handlers.user import enroll_user_from_deep_link
from settings import ADMIN_USER_IDS, TOKEN, SUPER_ADMIN_USER_IDS
from keyboards import reply, inline, builders 
from data.requests import (get_welcome, get_contacts, set_user, get_cases, get_case_by_id, get_services,
                           get_service_by_id, get_events, get_event_by_id, get_briefing, get_instructions)


admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"

class BriefingStates(StatesGroup):
    question = State()
    waiting_for_answer = State()
    send_report = State()


router = Router()


@router.message(CommandStart(deep_link_encoded=True))
async def cmd_start(message: Message, command: CommandObject):
    welcome = await get_welcome()
    user_id = message.from_user.id
    if isinstance(message, Message):
        await set_user(user_id, message.from_user.username)
    args = command.args
    payload = decode_payload(args)
    payload_parts = payload.split("_")
    payload_type = payload_parts[0]
    if payload_type == "event":
        event_id = payload_parts[1]
        await enroll_user_from_deep_link(message, user_id, event_id)
    elif payload_type == "days":
        days = int(payload_parts[1])
        await change_paid_days(days)
    if not welcome:
        await message.answer(f"👋Добро пожаловать, {message.from_user.first_name}!"
            "Выберите вариант из меню ниже👇", reply_markup=reply.user_main)
    else:
        await message.answer_photo(welcome.picture, welcome.about)
        await message.answer("Выберите вариант из меню ниже👇", reply_markup=reply.user_main)

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome = await get_welcome()
    user_id = message.from_user.id
    if isinstance(message, Message):
        await set_user(user_id, message.from_user.username)
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer(f"👋Добро пожаловать, администратор {message.from_user.first_name}! "
        "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇",
            reply_markup=reply.admin_main)
    elif message.from_user.id in SUPER_ADMIN_USER_IDS:
        await message.answer(f"👋Добро пожаловать, супер администратор {message.from_user.first_name}!")
    else:
        if not welcome:
            await message.answer(f"👋Добро пожаловать, {message.from_user.first_name}!"
                "Выберите вариант из меню ниже👇", reply_markup=reply.user_main)
        else:
            await message.answer_photo(welcome.picture, welcome.about)
            await message.answer("Выберите вариант из меню ниже👇", reply_markup=reply.user_main)
        
async def change_paid_days(days: int):
    settings.paid_days += days
        
@router.callback_query(F.data == "to_main")        
async def to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Выберите вариант из меню ниже👇", reply_markup=reply.user_main)

@router.message(F.text.lower() == "📖 контакты")
async def contact_selected(message: Message):
    contacts = await get_contacts()   
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    if len(contact_info) < 2:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("❌Вы ещё не добавили ни одного контакта", reply_markup=inline.new_contact)
        else:
            await message.answer("❌Контактная информация отсутствует")
    else:
        await message.answer(f"<b>📖Моя контактная информация и график работы:</b>\n{contact_info}")
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите желаемую опцию:👇", reply_markup=inline.contacts)
   
@router.message(F.text.lower() == "💎 кейсы")
async def cases_selected(message: Message):
    cases = await get_cases()
    cases_list = "\n".join([f"{case.title}" for case in cases])
    if len(cases_list) < 1:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("❌Вы ещё не добавили ни одного кейса", reply_markup=inline.new_case)
        else:
            await message.answer("❌Кейсы отсутствуют", reply_markup=reply.user_main)
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите кейс для изменения/удаления или добавьте новый👇", 
                             reply_markup=await builders.admin_get_cases())
        else:    
            await message.answer("Мои самые лучшие кейсы:", reply_markup=await builders.get_cases_kb())
    
@router.callback_query(F.data.startswith("cases_"))    
async def case_detail_selected(callback: CallbackQuery):
    case = await get_case_by_id(callback.data.split("_")[1])
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(f"<b>{case.title}</b>\n\n{case.description}", 
                                         reply_markup=await inline.case_chosen(case.id))
    else:
        await callback.message.edit_text(f"<b>{case.title}</b>\n\n{case.description}")
        
@router.message(F.text.lower() == "🤝 услуги")
async def service_selected(message: Message):
    services  = await get_services()
    services_list = "\n".join([f"{service.title}" for service in services])
    if len(services_list) < 2:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("❌Вы ещё не добавили ни одной услуги", reply_markup=inline.new_service)
        else:
            await message.answer("❌Услуги отсутствуют", reply_markup=reply.user_main)
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите услугу для изменения/удаления или добавьте новую👇",
                             reply_markup=await builders.admin_get_services())
        else:
            await message.answer("Мои самые выгодные услуги:", reply_markup=await builders.get_services_kb())
        
@router.callback_query(F.data.startswith("services_"))
async def service_detail_selected(callback: CallbackQuery):
    service = await get_service_by_id(callback.data.split("_")[1])
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(f"<b>{service.title}</b>\n\n{service.description}", 
                                         reply_markup=await inline.service_chosen(service.id))
    else:
        await callback.message.edit_text(f"<b>{service.title}</b>\n\n{service.description}",
                                         reply_markup=await inline.order_service(service.id))
               
@router.message(F.text.lower() == "📆 мероприятия")
async def event_selected(message: Message):
    events = await get_events()
    events_list = "\n".join([f"{event.title}" for event in events])
    if len(events_list) < 2:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("❌Вы ещё не добавили ни одного мероприятия", reply_markup=inline.new_event)
        else:
            await message.answer("❌Мероприятия отсутствуют", reply_markup=reply.user_main)
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите мероприятие для изменения/удаления или добавьте новое👇",
                             reply_markup=await builders.admin_get_events())
        else:
            await message.answer("👀Мои самые интересные мероприятия:", reply_markup=await builders.get_events_kb())
    
@router.callback_query(F.data.startswith("events_"))
async def event_detail_selected(callback: CallbackQuery, bot: Bot):
    event_id = callback.data.split("_")[1]
    event = await get_event_by_id(event_id)
    formatted_date = event.date.strftime('%Y-%m-%d %H:%M')
    deep_link = await create_start_link(bot, f'event_{event_id}', encode=True)
    event_for_admin = (f"<b>{event.title}</b>\n\n{event.description}\n\n<b>{formatted_date}</b>\n\n"
        f"🌐Ссылка на событие: {deep_link}")
    event_for_user = (f"<b>{event.title}</b>\n\n{event.description}\n\n<b>{formatted_date}</b>\n\n")
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(event_for_admin, reply_markup=await inline.event_chosen(event.id))
    else:
        await callback.message.edit_text(event_for_user, reply_markup=await inline.enroll_user(event.id))

async def show_instruction(message: Message):
    instructions = await get_instructions()
    default_instruction = (
        f"Этот брифинг создан, чтобы упростить наше будущее сотрудничество и не займет много Вашего времени")
    if message.from_user.id in ADMIN_USER_IDS:
        if instructions:
            instr_text = f"{instructions.description if instructions else None}"
        else:
            instr_text = default_instruction        
        return instr_text
    else:
        if instructions:
            await message.answer(text=instructions.description, reply_markup=inline.start_briefing)
        else:
            await message.answer(text=default_instruction, reply_markup=inline.start_briefing)

@router.message(F.text.lower() == "❓ брифинг")
async def briefing_selected(message: Message):
    briefing = await get_briefing()
    briefing_list = []
    for brief in briefing:
        answer = brief.answer if len(brief.answer) > 2 else "*Ответ в свободной форме*"
        briefing_list.append(f"{brief.id} {brief.question}\n{answer}")
    briefing_text = "\n".join(briefing_list)
    if briefing_text:
        if message.from_user.id in ADMIN_USER_IDS:
            parts = []
            while len(briefing_text) > 0:
                if len(briefing_text) <= 4000:
                    parts.append(briefing_text)
                    briefing_text = ""
                else:
                    cut_off = briefing_text.rfind("\n\n", 0, 4000)
                    if cut_off == -1:
                        cut_off = 4000 - briefing_text[0:4001][::-1].find("\n")
                    parts.append(briefing_text[:cut_off])
                    briefing_text = briefing_text[cut_off:].strip()
            instructions = await show_instruction(message)
            await message.answer(f"<b>❗Инструкции❗:</b>\n{instructions}\n<b>Весь брифинг:</b>")
            for part in parts:
                await message.answer(part)
            await message.answer("Выберите желаемое действие👇", reply_markup=inline.admin_get_briefing)
        else:
            await show_instruction(message)
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("❌Вы ещё не создали брифинг. Можем это сделать прямо сейчас👇", 
                                 reply_markup=inline.create_briefing)
        else:
            await message.answer("Брифинг отсутствует", reply_markup=reply.user_main)


@router.callback_query(F.data.startswith("cancel_"))
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user.id
    await callback.message.delete_reply_markup()
    await state.clear()
    await callback.answer("Операция отменена")
    if user in ADMIN_USER_IDS:
        await callback.message.answer(admin_hint, reply_markup=reply.admin_main)
    else:
        await callback.message.answer("Выберите вариант из меню ниже👇", reply_markup=reply.user_main)
        
