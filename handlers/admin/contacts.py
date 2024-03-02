from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import inline, reply, builders
from filters.is_admin import IsAdmin
from data.requests import set_contact, get_contacts, delete_contacts, edit_contact


admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"
router = Router()

contact_type_hint = ("Введите тип контактной информации. Например: Фамилия Имя Отчество; Телефон; Адрес; График "
"работы; Ссылка на сайт, или социальную сеть")

class AddContact(StatesGroup):
    contact_type = State()
    contact_value = State()


class EditContact(StatesGroup):
    _id = State()
    contact_type = State()
    contact_value = State()
    

@router.callback_query(IsAdmin(), F.data == "add_contact")
async def add_more_contact(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddContact.contact_type)
    await callback.message.edit_text(contact_type_hint, reply_markup=inline.cancel_action)

@router.message(IsAdmin(), AddContact.contact_type)
async def add_contact_type(message: Message, state: FSMContext):
    await state.update_data(contact_type=message.text)
    await state.set_state(AddContact.contact_value)
    await message.answer('Введите контактную информацию', reply_markup=inline.cancel_action)

@router.message(IsAdmin(), AddContact.contact_value)
async def add_contact_value(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await set_contact(data)
    await state.clear()
    await message.answer('Контактная информация успешно добавлена')
    contacts = await get_contacts()   
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    await message.answer(f"<b>Моя контактная информация и график работы:</b>\n{contact_info}", 
                         reply_markup=inline.contacts)
    
@router.callback_query(IsAdmin(), F.data == "edit_contacts")
async def edit_contacts(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.edit_text("Выберите контактную для изменения", 
                                  reply_markup=await builders.edit_contact())
    
@router.callback_query(IsAdmin(), F.data.startswith("edit_contact_"))
async def edit_contact_selected(callback: CallbackQuery, state: FSMContext):
    await state.update_data(_id=callback.data.split('_')[2])
    await state.set_state(EditContact.contact_type)
    await callback.message.edit_text(contact_type_hint, reply_markup=inline.cancel_action)
   
@router.message(IsAdmin(), EditContact.contact_type)
async def edit_contact_type(message: Message, state: FSMContext):
    await state.update_data(contact_type=message.text)
    await state.set_state(EditContact.contact_value)
    await message.answer('Введите контактную информацию', reply_markup=inline.cancel_action)
    
@router.message(IsAdmin(), EditContact.contact_value)
async def edit_contact_value(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await edit_contact(data)
    await state.clear()
    await message.answer('Контактная информация успешно изменена')
    contacts = await get_contacts()
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", 
                         reply_markup=inline.contacts)
    
@router.callback_query(IsAdmin(), F.data == "predelete_contact")
async def predelete_contact(callback: CallbackQuery):
    await callback.message.edit_text("Эта операция удалит всю контактную информацию. Вы уверены?",
                                  reply_markup=inline.confirm_delete_contacts)
    
@router.callback_query(IsAdmin(), F.data == "delete_contacts")
async def confirmed_delete_contacts(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.delete()
    await delete_contacts()
    await callback.answer("Контактная информацию успешно удалена")   
    await callback.message.answer(admin_hint, reply_markup=reply.admin_main)