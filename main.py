# версия 1.2
from aiogram import Bot, Dispatcher
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.database.models import async_main
from app.handlers import router
from app.admin import admin
from settings import TOKEN


scheduler = AsyncIOScheduler()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filemode='w',
    level=logging.ERROR, filename='bot.log')

async def main():
    await async_main()
    
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(admin, router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    await scheduler.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Работа бота завершена')
