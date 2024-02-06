from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.database.requests import get_users, set_contact, get_contacts, delete_contacts, edit_contacts


admin = Router()
contact_type_hint = "Введите тип контактной информации. Например: Фамилия, Имя, Отчество; Телефон; Адрес офиса; График работы; Ссылка на сайт, или социальные сети (Вводить по одной ссылке)"
admin_hint = f"Возможные команды:\n/newsletter - Сделать рассылку\n/add_contact - Добавить контактную информацию\n/add_case - Добавить Кейс\n/add_event - Добавить Мероприятие\n/add_service - Добавить Услугу\n/create_briefing - Создать брифинг"
                                         
class Newsletter(StatesGroup):
    message = State()


class AddContact(StatesGroup):
    contact_type = State()
    contact_value = State()


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
    
    
@admin.callback_query(AdminProtect(), F.data =="add_contact")
async def add_more_contact(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await state.set_state(AddContact.contact_type)
    await call.message.answer(contact_type_hint)

@admin.callback_query(AdminProtect(), F.data.startswith("edit_contact_"))
async def edit_contacts(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await edit_contacts(callback.data.split("_")[2])
    
@admin.callback_query(AdminProtect(), F.data == "delete_contact")
async def delete_contact(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.answer("Эта операция удалит всю контактную информацию. Вы уверены?",
                                  reply_markup=kb.confirm_delete_contacts)
    
@admin.callback_query(AdminProtect(), F.data == "confirmed_delete_contacts")
async def confirm_delete_contact(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await delete_contacts()
    await callback.answer("Контактная информацию успешно удалена")    

@admin.callback_query(AdminProtect(), F.data.startswith("cancel_"))
async def cancel_operation(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.answer("Операция отменена")

# @admin.callback_query(AdminProtect(), AddContact.category)
# async def add_item_category(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(category=callback.data.split('_')[1])
#     await state.set_state(AddContact.description)
#     await callback.answer('')
#     await callback.message.answer('Введите описание товара')


# @admin.message(AdminProtect(), AddContact.description)
# async def add_item_description(message: Message, state: FSMContext):
#     await state.update_data(description=message.text)
#     await state.set_state(AddContact.photo)
#     await message.answer('Отправьте фото товара')


# @admin.message(AdminProtect(), AddContact.photo, F.photo)
# async def add_item_photo(message: Message, state: FSMContext):
#     await state.update_data(photo=message.photo[-1].file_id)
#     await state.set_state(AddContact.price)
#     await message.answer('Введите цену товара')


# @admin.message(AdminProtect(), AddContact.price)
# async def add_item_price(message: Message, state: FSMContext):
#     await state.update_data(price=message.text)
#     data = await state.get_data()
#     await set_item(data)
#     await message.answer('Контакт успешно добавлен')
#     await state.clear()

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
