from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import inline, builders
from filters import IsAdmin
from data.requests import set_service, delete_service, edit_service


router = Router()


class AddService(StatesGroup):
    title = State()
    description = State()
    

class EditService(StatesGroup):
    _id = State()
    title = State()
    description = State()


@router.callback_query(IsAdmin(), F.data == "add_service")
async def add_service(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddService.title)
    await callback.message.edit_text(
        'Введите название услуги. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
        reply_markup=inline.cancel_action)

@router.message(IsAdmin(), AddService.title)
async def add_service_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    await state.set_state(AddService.description)
    await message.answer('Введите описание услуги', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), AddService.description)
async def add_service_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_service(data)
    await state.clear()
    await message.answer('Услуга успешно добавлена', reply_markup=await builders.admin_get_services())

@router.callback_query(IsAdmin(), F.data.startswith("delete_service_"))
async def delete_service_selected(callback: CallbackQuery):
    await delete_service(callback.data.split('_')[2])
    await callback.answer("Услуга успешно удалена")
    markup = await builders.admin_get_services()
    num_buttons = sum(len(row) for row in markup.inline_keyboard)
    if num_buttons > 2: 
        await callback.message.edit_text("Мои самые выгодные услуги", reply_markup=markup)
    else:
        await callback.message.edit_text("Вы ещё не добавили ни одной услуги", reply_markup=inline.new_service)

@router.callback_query(IsAdmin(), F.data.startswith("edit_service_"))
async def edit_service_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=callback.data.split('_')[2])
    await state.set_state(EditService.title)
    await callback.message.edit_text(
        'Введите новое название услуги. Для корректного отображения в меню его длина не должна превышать 40 знаков', 
        reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditService.title)
async def edit_service_title(message: Message, state: FSMContext):
    if len(message.text) > 40:
        await message.answer('Я же просил не больше 40 знаков. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    await state.update_data(title=message.text)
    await state.set_state(EditService.description)
    await message.answer('Введите описание услуги', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditService.description)
async def edit_service_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await edit_service(data)
    await state.clear()
    await message.answer('Услуга успешно изменена', reply_markup=await builders.admin_get_services())
