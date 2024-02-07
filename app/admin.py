from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.database.requests import get_users, set_contact, get_contacts, delete_contacts, edit_contact, set_case


admin = Router()
contact_type_hint = "Введите тип контактной информации. Например: Фамилия, Имя, Отчество; Телефон; Адрес офиса; График работы; Ссылка на сайт, или социальные сети (Вводить по одной ссылке)"
admin_hint = f"Возможные команды:\n\n/newsletter - Сделать рассылку\n\n/add_contact - Добавить контактную информацию\n\n/add_case - Добавить Кейс\n\n/add_event - Добавить Мероприятие\n\n/add_service - Добавить Услугу\n\n/create_briefing - Создать брифинг"
                                         
class Newsletter(StatesGroup):
    message = State()


class AddContact(StatesGroup):
    contact_type = State()
    contact_value = State()


class EditContact(StatesGroup):
    id = State()
    contact_type = State()
    contact_value = State()


class AddCase(StatesGroup):
    title = State()
    description = State()
    
    
class EditCase(StatesGroup):
    id = State()
    title = State()
    description = State()
        
class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [5348838446]


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: Message):
    await message.answer(admin_hint)

@admin.message(AdminProtect(), Command('add_contact'))
async def add_contact(message: Message, state: FSMContext):
    await state.set_state(AddContact.contact_type)
    await message.answer(contact_type_hint)

@admin.callback_query(AdminProtect(), F.data =="add_contact")
async def add_more_contact(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddContact.contact_type)
    await callback.message.edit_text(contact_type_hint)

@admin.message(AdminProtect(), AddContact.contact_type)
async def add_contact_type(message: Message, state: FSMContext):
    await state.update_data(contact_type=message.text)
    await state.set_state(AddContact.contact_value)
    await message.answer('Введите контактную информацию')

@admin.message(AdminProtect(), AddContact.contact_value)
async def add_contact_value(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await set_contact(data)
    await state.clear()
    await message.answer('Контактная информация успешно добавлена')
    contacts = await get_contacts()   
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", reply_markup=kb.contacts_kb)
    
@admin.callback_query(AdminProtect(), F.data == "edit_contacts")
async def edit_contacts(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите контактную для изменения", 
                                  reply_markup=await kb.edit_contact_kb())
    
@admin.callback_query(AdminProtect(), F.data.startswith("edit_contact_"))
async def start_edit_contact(callback: CallbackQuery, state: FSMContext):
    await state.update_data(id=callback.data.split('_')[2])
    print(str(callback.data.split('_')[2]))
    await state.set_state(EditContact.contact_type)
    await callback.message.edit_text(contact_type_hint)
   
@admin.message(AdminProtect(), EditContact.contact_type)
async def edit_contact_type(message: Message, state: FSMContext):
    await state.update_data(contact_type=message.text)
    await state.set_state(EditContact.contact_value)
    await message.answer('Введите контактную информацию')
    
@admin.message(AdminProtect(), EditContact.contact_value)
async def edit_contact_value(message: Message, state: FSMContext):
    await state.update_data(value=message.text)
    data = await state.get_data()
    await edit_contact(data)
    await state.clear()
    await message.answer('Контактная информация успешно изменена')
    contacts = await get_contacts()
    contact_info = "\n".join([f"{contact.contact_type}: {contact.value}" for contact in contacts])
    await message.answer(f"Моя контактная информация и график работы:\n{contact_info}", reply_markup=kb.contacts_kb)
    
@admin.callback_query(AdminProtect(), F.data == "delete_contact")
async def delete_contact(callback: CallbackQuery):
    await callback.message.edit_text("Эта операция удалит всю контактную информацию. Вы уверены?",
                                  reply_markup=kb.confirm_delete_contacts)
    
@admin.callback_query(AdminProtect(), F.data == "confirmed_delete_contacts")
async def confirm_delete_contact(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await delete_contacts()
    await callback.answer("Контактная информацию успешно удалена")    

@admin.message(AdminProtect(), Command('add_case'))
async def add_case(message: Message, state: FSMContext):
    await state.set_state(AddCase.title)
    await message.answer('Введите название кейса')
    
@admin.callback_query(AdminProtect(), F.data == "add_case")
async def add_more_case(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddCase.title)
    await callback.message.edit_text('Введите название кейса')
    
@admin.message(AdminProtect(), AddCase.title)
async def add_case_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddCase.description)
    await message.answer('Введите описание кейса')

@admin.message(AdminProtect(), AddCase.description)
async def add_case_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    await set_case(data)
    await state.clear()
    await message.answer('Кейс успешно добавлен', reply_markup= await kb.get_cases_keyboard)
    await message.answer("Выберите желаемую опцию:", reply_markup = kb.add_case_kb)

@admin.callback_query(AdminProtect(), F.data == "delete_case")
async def delete_case(callback: CallbackQuery):
    pass








@admin.message(AdminProtect(), Command('newsletter'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям')
    

@admin.message(AdminProtect(), Newsletter.message)
async def newsletter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка.')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Рассылка успешно завершена.')
    await state.clear()

@admin.callback_query(AdminProtect(), F.data.startswith("cancel_"))
async def cancel_operation(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.answer("Операция отменена")
    await callback.message.answer(admin_hint)