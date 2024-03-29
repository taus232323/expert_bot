# версия 2.3
from aiogram import Bot, Dispatcher
import asyncio
import logging

from data.models import async_main
from handlers import common, user, superadmin
from handlers.admin import events, briefing, cases, contacts, newsletter, services, welcome, support
from handlers.admin.events import restart_event_reminders, events_scheduler
from handlers.admin.support import days_scheduler, schedule_decrease_paid_days
from handlers import superadmin
from settings import TOKEN



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',filemode='w',
    level=logging.ERROR, filename='bot.log')

async def main():
    await async_main()
    
    bot = Bot(token=TOKEN)
    bot.default.parse_mode = 'HTML'
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
        support.router,
        superadmin.router
        )
    
    await restart_event_reminders()
    events_scheduler.start()
    
    await schedule_decrease_paid_days()
    days_scheduler.start()
    
    await dp.start_polling(bot)
            

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Работа бота завершена')
