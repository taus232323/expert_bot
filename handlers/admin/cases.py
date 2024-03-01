from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import inline, builders
from filters import IsAdmin
from data.requests import set_case, delete_case, edit_case


class AddCase(StatesGroup):
    title = State()
    description = State()
    
    
class EditCase(StatesGroup):
    _id = State()
    title = State()
    description = State()
    
    
router = Router()
admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"


@router.callback_query(IsAdmin(), F.data == "add_case")
async def add_more_case(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCase.title)
    await callback.message.edit_text(
        'Введите название кейса. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
                                     reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), AddCase.title)
async def add_case_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    await state.set_state(AddCase.description)
    await message.answer('Введите описание кейса', reply_markup=inline.cancel_action)

@router.message(IsAdmin(), AddCase.description)
async def add_case_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_case(data)
    await state.clear()
    await message.answer('Кейс успешно добавлен', reply_markup=await builders.admin_get_cases())

@router.callback_query(IsAdmin(), F.data.startswith("delete_case_"))
async def delete_case_selected(callback: CallbackQuery):
    await delete_case(callback.data.split('_')[2])
    await callback.answer("Кейс успешно удалён", reply_markup=await builders.admin_get_cases())
    markup = await builders.admin_get_cases_kb()
    num_buttons = sum(len(row) for row in markup.inline_keyboard)
    if num_buttons > 2: 
        await callback.message.edit_text("Мои самые лучшие кейсы", reply_markup=markup)
    else:
        await callback.message.edit_text("Вы ещё не добавили ни одного кейса", reply_markup=inline.new_case)
    
@router.callback_query(IsAdmin(), F.data.startswith("edit_case_"))
async def edit_case_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(_id=callback.data.split('_')[2])
    await state.set_state(EditCase.title)
    await callback.message.edit_text(
        'Введите новое название кейса. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
                                     reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditCase.title)
async def edit_case_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    await state.set_state(EditCase.description)
    await message.answer('Введите описание кейса', reply_markup=inline.cancel_action)

@router.message(IsAdmin(), EditCase.description)
async def edit_case_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await edit_case(data)
    await state.clear()
    await message.answer('Кейс успешно изменён', reply_markup=await builders.admin_get_cases_kb())