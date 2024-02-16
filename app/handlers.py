from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from settings import ADMIN_USER_IDS
import app.keyboards as kb
from app.database.requests import (
    get_welcome, get_contacts, set_user, get_cases, get_case_by_id, get_services, get_service_by_id, 
    get_events, get_event_by_id, set_participant, get_briefing, get_instructions, add_response,
    delete_user_briefing, get_user_briefing, get_users,
    )


class BriefingStates(StatesGroup):
    question = State()
    waiting_for_answer = State()
    send_report = State()


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    if isinstance(message, Message):
        await set_user(message.from_user.id, message.from_user.username)
    if message.from_user.id in ADMIN_USER_IDS:
        await message.answer(f"Добро пожаловать, администратор {message.from_user.first_name}!"
            "Нажмите на кнопку в меню для просмотра, добавления или изменения информации", reply_markup=kb.user_main)
    else:
        welcome = await get_welcome()
        if not welcome:
            await message.answer(f"Добро пожаловать, {message.from_user.first_name}! Выберите вариант из меню ниже", 
                             reply_markup=kb.user_main)
        else:
            await message.answer_photo(welcome.picture, welcome.about)
            await message.answer("Выберите вариант из меню ниже", reply_markup=kb.user_main)
        

@router.callback_query(F.data == "to_main")        
async def to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(f"Выберите вариант из меню ниже", reply_markup=kb.user_main)

    
@router.message(F.text == "Контакты")
async def contact_selected(message: Message):
    contacts = await get_contacts()   
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    if len(contact_info) < 2:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Вы ещё не добавили ни одного контакта", reply_markup=kb.new_contacts_kb)
        else:
            await message.answer("Контактная информация отсутствует")
    else:
        await message.answer(f"Моя контактная информация и график работы:\n{contact_info}")
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите желаемую опцию:", reply_markup=kb.contacts_kb)
   
@router.message(F.text == "Кейсы")
async def cases_selected(message: Message):
    cases = await get_cases()
    cases_list = "\n".join([f"{case.title}" for case in cases])
    if len(cases_list) < 2:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Вы ещё не добавили ни одного кейса", reply_markup=kb.new_cases_kb)
        else:
            await message.answer("Кейсы отсутствуют")
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите кейс для изменения/удаления или добавьте новый", 
                             reply_markup=await kb.admin_get_cases_keyboard())
        else:    
            await message.answer("Мои самые лучшие кейсы:", reply_markup=await kb.get_cases_keyboard())
    
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
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Вы ещё не добавили ни одной услуги", reply_markup=kb.new_services_kb)
        else:
            await message.answer("Услуги отсутствуют")
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите услугу для изменения/удаления или добавьте новую",
                             reply_markup=await kb.admin_get_services_keyboard())
        else:
            await message.answer("Мои самые выгодные услуги:", reply_markup=await kb.get_services_keyboard())
        
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
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Вы ещё не добавили ни одного мероприятия", reply_markup=kb.new_events_kb)
        else:
            await message.answer("Мероприятия отсутствуют")
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Выберите мероприятие для изменения/удаления или добавьте новое",
                             reply_markup=await kb.admin_get_events_keyboard())
        else:
            await message.answer("Мои самые интересные мероприятия:", reply_markup=await kb.get_events_keyboard())
    
@router.callback_query(F.data.startswith("events_"))
async def event_detail_selected(callback: CallbackQuery):
    event_id = callback.data.split("_")[1]
    event = await get_event_by_id(event_id)
    formatted_date = event.date.strftime('%Y-%m-%d %H:%M')
    event_for_send = f"<b>{event.title}</b>\n\n{event.description}\n\n<b>{formatted_date}</b>"
    if callback.from_user.id in ADMIN_USER_IDS:
        await callback.message.edit_text(event_for_send, reply_markup=await kb.event_chosen_keyboard(event.id))
    else:
        await callback.message.edit_text(event_for_send, reply_markup=await kb.enroll_user_keyboard(event.id))

@router.callback_query(F.data.startswith("enroll_"))
async def enroll_user(callback: CallbackQuery):
    event_id = callback.data.split("_")[2]
    event = await get_event_by_id(event_id)
    tg_id = callback.from_user.id
    formatted_date = event.date.strftime('%Y-%m-%d %H:%M')
    event_details = f"\n<b>{event.title}</b>.\nДата и время события: \n<b>{formatted_date}</b>"
    success_message = f"Вы успешно записаны на:{event_details}"
    is_in_event = f"Вы уже записаны на:{event_details}"
    participant_added = await set_participant(tg_id=tg_id, event_id=event_id)
    if participant_added is True:
        await callback.message.delete()
        await callback.message.answer(success_message, reply_markup=kb.user_main)
    else:
        await callback.message.delete()
        await callback.message.answer(is_in_event, reply_markup=kb.user_main)

async def show_instruction(message: Message):
    instructions = await get_instructions()
    default_instruction = f"<b>Вы не добавили инструкцию. По умолчанию она такая:</b>\n Этот брифинг создан, чтобы упростить наше будущее сотрудничество и не займет много Вашего времени"
    if message.from_user.id in ADMIN_USER_IDS:
        if instructions:
            instr_text = f"{instructions.description if instructions else None}"
        else:
            instr_text = default_instruction        
        return instr_text
    else:
        if instructions:
            await message.answer(text=instructions.description, reply_markup=await kb.start_briefing_kb())
        else:
            await message.answer(text=default_instruction, reply_markup=kb.start_briefing_kb)

@router.callback_query(F.data == "briefing")
@router.message(F.text == "Пройти опрос")
async def briefing_selected(message: Message):
    briefing = await get_briefing()
    briefing_list = []
    for brief in briefing:
        answer = brief.answer if len(brief.answer) > 2 else "*Ответ в свободной форме*"
        briefing_list.append(f"{brief.id} {brief.question}\n{answer}")
    briefing_text = "\n".join(briefing_list)
    if briefing_text:
        if message.from_user.id in ADMIN_USER_IDS:
            instructions = await show_instruction(message)
            await message.answer(f"<b>Инструкции:</b>\n{instructions}\n<b>Весь брифинг:</b>\n\n{briefing_text}",
                                     reply_markup=kb.admin_get_briefing_kb)
        else:
            await show_instruction(message)
    else:
        if message.from_user.id in ADMIN_USER_IDS:
            await message.answer("Вы ещё не создали брифинг. Можем это сделать прямо сейчас", 
                                 reply_markup=kb.create_briefing_kb)
        else:
            await message.answer("Брифинг отсутствует", reply_markup=kb.user_main)

@router.callback_query(F.data == "start_briefing")
async def start_briefing(callback: CallbackQuery, state: FSMContext):
    await delete_user_briefing(callback.from_user.id)
    await state.update_data(current_question_index=0, response=[])
    await state.set_state(BriefingStates.question)

@router.message(BriefingStates.question)
async def send_next_question(callback: CallbackQuery, state: FSMContext):
    briefing = await get_briefing()
    briefing_questions = briefing.scalars().all()
    data = await state.get_data()
    current_index = data['current_question_index']
    if current_index < len(briefing_questions):
        question = briefing_questions[current_index]
        markup = kb.generate_markup(question.answer)
            
        await callback.message.answer(question.question, reply_markup=markup)
        await state.set_state(BriefingStates.waiting_for_answer)
    else:
        await callback.message.answer("Брифинг завершен, спасибо за ваши ответы!", 
                                          reply_markup=kb.generate_end_markup())
        await send_report()
        
@router.message(BriefingStates.waiting_for_answer)
async def briefing_answer_received(message: Message, state: FSMContext):
    await state.update_data(response=message.text)
    await message.answer(f"Ваш ответ: {message.text}", reply_markup=kb.in_briefing_kb)
    
@router.callback_query(F.data == 'continue')
async def continue_briefing(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_response(data)
    next_index = data['current_question_index'] + 1
    await state.update_data(current_question_index=next_index, response=[])
    await state.set_state(BriefingStates.question)

@router.callback_query(F.data == 'edit_answer')
async def change_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_response(data)
    next_index = data['current_question_index'] - 1
    await state.update_data(current_question_index=next_index, response=[])
    await state.set_state(BriefingStates.question)
  
@router.callback_query(F.data =='restart_briefing')
async def restart_briefing(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await start_briefing(callback, state)

@router.callback_query(F.data == 'preend_briefing')
async def preend_briefing(callback: CallbackQuery):
    await callback.message.edit_text(
        'Брифинг не завершён, ответы не будут сохранены. Если вы хотите продолжить, нажмите кнопку "Вернуться"',
        reply_markup=kb.generate_end_markup())

@router.callback_query(F.data == 'resume_briefing')
async def resume_briefing(callback: CallbackQuery):
    await callback.message.delete()

@router.callback_query(F.data =='end_briefing')
async def finish_briefing_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Брифинг завершён, спасибо за участие.", reply_markup=kb.user_main)
    await state.set_state(BriefingStates.send_report)
    
async def prepare_report(message: Message):
    briefing  = await get_user_briefing(message.from_user.id)
    briefing_list = []
    for brief in briefing:
        briefing_list.append(f"{brief.id} {brief.question}\n{brief.answer}")
    briefing_text = "\n".join(briefing_list)
    parts = []
    current_part = ""
    for chunk in briefing_list:
        if len(chunk) + 1 < 4000:
                return chunk
        else:
            last_double_newline = current_part.rfind("\n\n", 0, 4000)
            if last_double_newline != -1:
                parts.append(current_part[:last_double_newline])
                current_part = current_part[last_double_newline + 2:] + chunk + "\n"
            else:
                parts.append(current_part[:4000])
                current_part = current_part[4000:] + chunk + "\n"
    if current_part:
        parts.append(current_part)
    return parts

@router.message(BriefingStates.send_report)     
async def send_report(message: Message, state: FSMContext):
    await state.clear()
    user = await get_users(message.from_user.id)
    report = await prepare_report(message)
    if isinstance(report, list):
        first_part = report[0]
        for admin in ADMIN_USER_IDS:
            await message.answer(admin, f"<b>Заполненный брифинг от\n{user.username}:</b>\n\n{first_part}")
        for part in report and admin in ADMIN_USER_IDS:
                await message.answer(admin, f"<b>Продолжение брифинга от\n{user.username}:</b>\n\n{part}")
    else:
        for admin in ADMIN_USER_IDS:
            await message.answer(admin, f"<b>Заполненный брифинг от\n{user.username}:</b>\n\n{report}")
        
      
        
@router.message()
async def echo(message: Message):
    await message.answer(f"Я не понимаю, что вы хотите")