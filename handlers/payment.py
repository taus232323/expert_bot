from aiogram import Router, Bot
from aiogram.types import Message, PreCheckoutQuery, ContentType, LabeledPrice
from aiogram.filters import Command

from settings import PAYMENTS_TOKEN, ADMIN_USER_IDS

paid_days = 0
router = Router()
one_month_price = LabeledPrice(label="Подписка на 1 месяц", amount=200*100)
# three_month_price = LabeledPrice(label="Подписка на 3 месяца", amount=400*100)
# six_month_price = LabeledPrice(label="Подписка на полгода", amount=800*100)
# year_price = LabeledPrice(label="Подписка на 1 год", amount=1000*100)

@router.message(Command('buy'))
async def buy(message: Message, bot: Bot):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await message.answer("Тестовый платеж!!!")

    await bot.send_invoice(chat_id=message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[one_month_price],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload",
                           need_name=True,
                           need_phone_number=True)
    print('sent')

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@router.message()
async def payment_handler(message: Message):
    if message.content_type == ContentType.SUCCESSFUL_PAYMENT:
        print("SUCCESSFUL PAYMENT:")
        payment_info = message.successful_payment.to_python()
        for k, v in payment_info.items():
            print(f"{k} = {v}")

        currency = message.successful_payment.currency
        total_amount = message.successful_payment.total_amount // 100 
        await message.answer(f"Платеж на сумму {total_amount} {currency} прошёл успешно!!!")