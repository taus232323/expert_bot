from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from keyboards import inline, reply
from filters.is_admin import IsAdmin
from data.requests import get_welcome, set_welcome, edit_welcome, delete_welcome


admin_hint = "Нажмите на кнопку в меню для просмотра, добавления или изменения информации👇"
router = Router()

class AddWelcome(StatesGroup):
    picture = State()
    about = State()


class EditWelcome(StatesGroup):
    _id = State()
    picture = State()
    about = State()    
    

@router.message(IsAdmin(), F.text.lower() == "👋 тг-визитка")    
async def welcome_selected(message: Message):
    welcome = await get_welcome()
    if welcome:
        await message.answer_photo(welcome.picture, welcome.about, reply_markup=inline.edit_welcome)
    else:
        await message.answer('Вы ещё не добавили телеграм-визитку(это первое что я напишу Вашему '
                             'клиенту поле того, как он нажмёт кнопку START). Хотите сделать это сейчас?',
                             reply_markup=inline.new_welcome)
        
@router.callback_query(IsAdmin(), F.data == "add_welcome")
async def add_welcome(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'📷 Для начала отправьте своё самое лучшее фото!\n\n'
        '⚠️ Подробная инструкция и показательные примеры приветствия (телеграм-визитки) '
        'Вы найдете на нашем канале @botpbu - перейдите в закрепленное сообщение на канале и '
        'выберете хештег #Телеграмвизитка', reply_markup=inline.cancel_action)
    await  state.set_state(AddWelcome.picture)

@router.message(IsAdmin(), AddWelcome.picture)
async def add_welcome_picture(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(picture=message.photo[-1].file_id)
        await state.set_state(AddWelcome.about)
        await message.answer(
    'Теперь расскажите вкратце кто Вы  и чем занимаетесь. Остальное мы позже добавим в соответствующие пункты меню', 
                        reply_markup=inline.cancel_action)
    else:
        await message.answer('Вы отправили не самое лучшее фото, или отменили сжатие. Попробуйте ещё раз',
                             reply_markup=inline.cancel_action)
        return
    
@router.message(IsAdmin(), AddWelcome.about)
async def add_welcome_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()
    await set_welcome(data)
    await state.clear()
    await message.answer(
        'Приветственное сообщение успешно добавлено. Теперь можно добавить информацию в другие пункты меню ниже', 
        reply_markup=reply.admin_main)
    
@router.callback_query(IsAdmin(), F.data == "edit_welcome")
async def edit_welcome_selected(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer('📷 Пришлите фото которое ещё лучше предыдущего!', reply_markup=inline.cancel_action)
    await state.set_state(EditWelcome.picture)
    
@router.message(IsAdmin(), EditWelcome.picture)
async def edit_welcome_picture(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(picture=message.photo[-1].file_id)
        await state.set_state(EditWelcome.about)
        await message.answer(
            'Теперь добавьте более актуальную и интересную информацию о себе', reply_markup=inline.cancel_action)
    else:
        await message.answer('Вы отправили не самое лучшее фото, или отменили сжатие. Попробуйте ещё раз', 
                             reply_markup=inline.cancel_action)
        return
    
@router.message(IsAdmin(), EditWelcome.about)
async def edit_welcome_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()
    await edit_welcome(data)
    await state.clear()
    await message.answer(
        'Приветственное сообщение успешно изменено. Теперь можно добавить информацию в другие пункты меню ниже',
        reply_markup=reply.admin_main)
    
@router.callback_query(IsAdmin(), F.data == "predelete_welcome")
async def predelete_welcome(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.answer('Вы уверены что хотите удалить приветственное сообщение?',
                                     reply_markup=inline.confirm_delete_welcome)
    
@router.callback_query(IsAdmin(), F.data == "delete_welcome")
async def confirmed_delete_welcome(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.delete()
    await delete_welcome()
    await callback.answer('Приветственное сообщение успешно удалено')
    await callback.message.answer(admin_hint, reply_markup=reply.admin_main)