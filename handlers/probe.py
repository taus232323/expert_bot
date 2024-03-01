
# async def decrease_counter():
#     global days_remaining
#     if days_remaining > 0:
#         days_remaining -= 1
#     else:
#         ADMIN_USER_IDS = ADMIN_USER_IDS[:2]
    
# async def start_rent_counter(message: Message):
#     msg = await message.answer(f"Оплачено дней аренды: {days_remaining}")
#     message_id = msg.message_id
#     await message.pin()
#     scheduler.add_job(decrease_counter, 'cron', hour=0)
#     try:
#         await message.edit_text(message_id=message_id, text=f"Оплачено дней аренды: {days_remaining}")
#     except Exception as e:
#         print(f"Ошибка при обновлении счётчика: {e}")
#     scheduler.start()
    