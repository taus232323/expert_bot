from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import inline
from filters.is_admin import IsAdmin
from data.requests import (set_instructions, edit_instructions, delete_instructions, get_briefing, 
add_question, edit_question, get_instructions, delete_briefing)


router = Router()


class AddInstruction(StatesGroup):
    description = State()


class EditInstruction(StatesGroup):
    _id = State()
    description = State()
    
    
class AddBriefing(StatesGroup):
    question = State()
    answer = State()


class EditBriefing(StatesGroup):
    _id = State()
    question = State()
    answer = State()
    
    
@router.callback_query(IsAdmin(), F.data == "instruction")
async def instruction(callback: CallbackQuery):
    instructions = await get_instructions()
    default_instruction = (f"<b>Вы не добавили инструкцию. По умолчанию она такая:</b>\n Этот брифинг создан, "
                           "чтобы упростить наше будущее сотрудничество и не займет много Вашего времени")
    if instructions:
        instr_text = f"{instructions.description if instructions else None}"
        await callback.message.edit_text(instr_text, reply_markup=inline.edit_instruction)
    else:
        instr_text = default_instruction        
        await callback.message.edit_text(instr_text, reply_markup=inline.new_instruction)

@router.callback_query(IsAdmin(), F.data == "add_instruction")
async def add_instruction(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddInstruction.description)
    await callback.message.edit_text('Введите свою инструкцию по прохождению брифинга', reply_markup=inline.cancel_action)

@router.message(IsAdmin(), AddInstruction.description)
async def save_instruction(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_instructions(data)
    await state.clear()
    await message.answer("Инструкция сохранена. Теперь можно приступить к созданию брифнга", 
                         reply_markup=inline.in_create_briefing) 

@router.callback_query(IsAdmin(), F.data == "edit_instruction")
async def edit_instruction(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditInstruction.description)
    await callback.message.edit_text('Введите новую инструкцию по прохождению брифинга', reply_markup=inline.cancel_action)

@router.message(IsAdmin(), EditInstruction.description)
async def edit_instruction(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await edit_instructions(data)
    await state.clear()
    await message.answer("Инструкция изменена. Теперь можно приступить к созданию брифнга", 
                         reply_markup=inline.in_create_briefing)
        
@router.callback_query(IsAdmin(), F.data == "delete_instruction")
async def delete_instruction(callback: CallbackQuery):
    await delete_instructions()
    await callback.message.edit_text('Инструкция удалена', reply_markup=inline.create_briefing)

@router.callback_query(IsAdmin(), F.data == "create_briefing")
async def create_briefing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Сейчас Вы будете создавать брифинг следуйте моим инструкциям и у Вас всё получится')
    await state.set_state(AddBriefing.question)
    await callback.message.answer('Введите текст вопроса', reply_markup=inline.cancel_action)

@router.message(IsAdmin(), AddBriefing.question)
async def add_briefing_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(AddBriefing.answer)
    await message.answer('Введите варианты ответов через знак точки с запятой ";", либо знак минус '
                         '"-" если хотите, чтобы ответ был в свободной форме', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), AddBriefing.answer)    
async def add_briefing_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    await add_question(data)
    await state.clear()
    await message.answer("Вопрос добавлен. Хотите посмотреть что получилось или добавить ещё один?",
                         reply_markup=inline.in_create_briefing)

@router.callback_query(IsAdmin(), F.data == "view_briefing")
async def view_briefing(callback: CallbackQuery):
    briefing = await get_briefing()
    instructions = await get_instructions()
    default_instruction = (
        "Этот брифинг создан, чтобы упростить наше будущее сотрудничество и не займет много Вашего времени")
    if instructions:
        instr_text = f"{instructions.description if instructions else None}"
    else:
        instr_text = default_instruction
    briefing_list = []
    for brief in briefing:
        answer = brief.answer if len(brief.answer) > 2 else "*Ответ в свободной форме*"
        briefing_list.append(f"{brief.id} {brief.question}\n{answer}")
    briefing_text = "\n".join(briefing_list)
    if briefing_text:
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
        await callback.message.answer(f"<b>Инструкции:</b>\n{instr_text}\n<b>Весь брифинг:</b>")
        for part in parts:
            await callback.message.answer(part)
        await callback.message.answer("Выберите желаемое действие", reply_markup=inline.admin_get_briefing)
    else:
        await callback.message.edit_text(
            f"<b>Инструкции:</b>\n{instr_text}\n\nА брифинг нужно создать. Сделаем это сейчас?", 
            reply_markup=inline.create_briefing)    
        
@router.callback_query(IsAdmin(), F.data == "add_question")
async def add_question_to_briefing(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddBriefing.question)
    await callback.message.edit_text('Введите текст вопроса', reply_markup=inline.cancel_action)

@router.callback_query(IsAdmin(), F.data == "edit_briefing")
async def edit_briefing(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.answer('Хотите добавить новый вопрос, изменить существующий или удалить брифинг целиком?', 
                                     reply_markup=inline.edit_briefing)

@router.callback_query(IsAdmin(), F.data == "predelete_briefing")
async def predelete_briefing(callback: CallbackQuery):
    warning = 'Эта операция удалит весь брифинг вместе с ответами пользователей, '
    'но вы можете изменить вопросы по отдельности'
    await callback.message.edit_text(warning, reply_markup=inline.confirm_delete_briefing)
    
@router.callback_query(IsAdmin(), F.data == "delete_briefing")
async def confirmed_delete_briefing(callback: CallbackQuery):
    await delete_briefing()
    await callback.message.edit_text('Брифинг удалён', reply_markup=inline.create_briefing)

@router.callback_query(IsAdmin(), F.data == "edit_question")
async def edit_question_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditBriefing._id)
    await callback.message.edit_text('Введите номер вопроса, который Вы желаете изменить', 
                                     reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditBriefing._id)
async def edit_question_selected(message: Message, state: FSMContext):
    await state.update_data(_id=message.text)
    await state.set_state(EditBriefing.question)
    await message.answer('Введите новый вопрос', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditBriefing.question)
async def edit_question_text(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await state.set_state(EditBriefing.answer)
    await message.answer('Введите новые варианты ответа через знак точки с запятой ";", либо знак минус '
                         '"-" если хотите, чтобы ответ был в свободной форме',
                         reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditBriefing.answer)
async def edit_question_answer(message: Message, state: FSMContext):
    await state.update_data(answer=message.text)
    data = await state.get_data()
    await edit_question(data)
    await state.clear()
    await message.answer('Вопрос изменён. Хотите посмотреть что получилось или добавить ещё один?', 
                         reply_markup=inline.in_create_briefing)