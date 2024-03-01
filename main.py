# версия 1.4
from aiogram import Bot, Dispatcher
import asyncio
import logging

from data.models import async_main
from handlers import common, user, superadmin
from handlers.admin import events, briefing, cases, contacts, newsletter, services, welcome
from handlers.admin.events import schedule_reminders
from handlers.superadmin import superadmin
from settings import TOKEN



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filemode='w',
    level=logging.ERROR, filename='bot.log')

async def main():
    await async_main()
    
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(
        common.router,
        events.router,
        contacts.router,
        services.router,
        welcome.router,
        cases.router,
        newsletter.router,
        briefing.router,
        user.router,
        superadmin.router,       
        )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    await schedule_reminders()
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Работа бота завершена')
