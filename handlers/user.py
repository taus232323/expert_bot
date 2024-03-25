from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.exceptions import TelegramForbiddenError


from keyboards import reply, inline, builders 
from data.requests import (get_user_by_id, set_participant, set_response, get_service_by_id, get_admins,
    delete_user_briefing, get_user_briefing, get_question_by_id, get_user_by_tg, get_event_by_id, get_paid_days,
    get_last_question_number)

class BriefingStates(StatesGroup):
    question = State()
    waiting_for_answer = State()
    send_report = State()


router = Router()


async def enroll_user_from_deep_link(message: Message, tg_id, event_id):
    print(f"Enrolling user {tg_id} to event {event_id}")
    event = await get_event_by_id(event_id)
    formatted_date = event.date.strftime('%d-%m-%Y- %H:%M')
    event_details = f"\n<b>{event.title}</b>.\n🗓Дата и время события: \n<b>{formatted_date}</b>"
    success_message = f"✅Вы успешно записаны на:{event_details}"
    is_in_event = f"✳Вы уже записаны на:{event_details}"
    participant_added = await set_participant(tg_id=tg_id, event_id=event_id)
    if participant_added is True:
        await message.answer(success_message, reply_markup=reply.user_main)
    else:
        await message.answer(is_in_event, reply_markup=reply.user_main)
     
@router.callback_query(F.data.startswith("order_service_"))
async def order_service(callback: CallbackQuery, bot: Bot):
    ADMIN_USER_IDS = await get_admins()
    service = await get_service_by_id(callback.data.split("_")[2])
    user = callback.from_user.username
    await callback.message.edit_text(
        f"🤝Вы заказали услугу <b>{service.title}</b>. Я Вам напишу в самое ближайшее время")
    for admin in ADMIN_USER_IDS:
        with suppress(TelegramForbiddenError):
            await bot.send_message(chat_id=admin, 
        text=f"👍Заказ услуги <b>{service.title}</b> от @{user}. Этот клиент очень хочет, чтобы Вы ему написали🙏")
            
@router.callback_query(F.data.startswith("enroll_"))
async def enroll_user(callback: CallbackQuery):
    event_id = callback.data.split("_")[2]
    event = await get_event_by_id(event_id)
    tg_id = callback.from_user.id
    formatted_date = event.date.strftime('%d-%m-%Y %H:%M')
    event_details = f"\n<b>{event.title}</b>.\n🗓Дата и время события: \n<b>{formatted_date}</b>"
    success_message = f"✅Вы успешно записаны на:{event_details}"
    is_in_event = f"☑Вы уже записаны на:{event_details}"
    participant_added = await set_participant(tg_id=tg_id, event_id=event_id)
    if participant_added is True:
        await callback.message.delete()
        await callback.message.answer(success_message, reply_markup=reply.user_main)
    else:
        await callback.message.delete()
        await callback.message.answer(is_in_event, reply_markup=reply.user_main)
        
            
@router.callback_query(F.data == "start_briefing")
async def start_briefing(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.message.delete_reply_markup()
    await delete_user_briefing(user_id)
    user = await get_user_by_tg(user_id)
    await state.update_data(user=user.id, question=1, answer=[])
    await state.set_state(BriefingStates.question)
    await callback.answer()
    await send_next_question(callback.message, state)

@router.message(BriefingStates.question)
async def send_next_question(message: Message, state: FSMContext):
    data = await state.get_data()
    current_index = data['question']
    max_questions = await get_last_question_number()
    if current_index <= max_questions:
        print('while')
        question = await get_question_by_id(current_index)
        answers = await builders.generate_answer(current_index)  
        await message.answer(question, reply_markup=answers)
        await state.set_state(BriefingStates.waiting_for_answer)
    else:
        await message.answer("Брифинг завершен, спасибо за ваши ответы!🤝",
                                          reply_markup=inline.briefing_finished)
        await send_report(message, state)
        
@router.message(BriefingStates.waiting_for_answer)
async def briefing_answer_received(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    await message.answer(f"Ваш ответ: {message.text}", reply_markup=inline.in_briefing)
    
@router.callback_query(F.data == 'continue')
async def continue_briefing(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    next_question = data['question'] + 1
    await state.update_data(answer=data['answer'], question=next_question)
    await set_response(data)
    await state.set_state(BriefingStates.question)
    await send_next_question(callback.message, state)

@router.callback_query(F.data == 'edit_answer')
async def change_answer(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(BriefingStates.question)
    await send_next_question(callback.message, state)
  
@router.callback_query(F.data =='restart_briefing')
async def restart_briefing(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await start_briefing(callback, state)

@router.callback_query(F.data == 'preend_briefing')
async def preend_briefing(callback: CallbackQuery):
    await callback.message.edit_text(
        '❗Брифинг не завершён, ответы не будут сохранены. Если вы хотите продолжить, нажмите кнопку "Вернуться"',
        reply_markup=inline.end_briefing_selected)

@router.callback_query(F.data == 'resume_briefing')
async def resume_briefing(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(BriefingStates.question)
    await send_next_question(callback.message, state)

@router.callback_query(F.data =='end_briefing')
async def finish_briefing_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Брифинг завершён, спасибо за участие🤝", reply_markup=inline.briefing_finished)
    await send_report(callback.message, state)
    
async def prepare_report(state: FSMContext):
    data = await state.get_data()
    user = data['user']
    briefing_records = await get_user_briefing(user)
    briefing_list = [f"{brief[0]}\n{brief[1]}" for brief in briefing_records]
    briefing_text = "\n\n".join(briefing_list)
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
    return parts

async def send_report(message: Message, state: FSMContext):
    data = await state.get_data()
    user = data['user']
    days = await get_paid_days()
    ADMIN_USER_IDS = await get_admins() if days >= 1 else []
    report = await prepare_report(state)
    user_briefing = await get_user_by_id(user)
    username = user_briefing.username
    await state.clear()
    try:
        first_part = report[0]
        left_parts = report[1:]
    except IndexError:
        print('IndexError')
    for admin in ADMIN_USER_IDS:
        try:    
            if len(report) > 1:
                await message.bot.send_message(
                    chat_id=admin, text=f"<b>✅✅✅Заполненный брифинг от✅✅✅</b>\n@{username}:\n\n{first_part}")
                for part in left_parts:
                    await message.bot.send_message(
                        chat_id=admin, text=f"<b>✔✔✔Продолжение брифинга от✔✔✔</b>\n@{username}:\n\n{part}")
            else:
                await message.bot.send_message(
                    chat_id=admin, text=f"<b>✅✅✅Заполненный брифинг от✅✅✅</b>\n@{username}:\n\n{report[0]}")
        except TelegramForbiddenError:
            print(f'Не удалось отправить сообщение админу {admin}')