from aiogram.types import LabeledPrice
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command

from settings import PAYMENTS_TOKEN

router = Router()
PRICE = LabeledPrice(label="Подписка на 1 месяц", amount=2000*100)

@router.message(Command('buy'))
async def buy(message: Message):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await message.answer("Тестовый платеж!!!")

    await message.invoice(
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")

