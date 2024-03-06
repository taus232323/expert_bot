from aiogram.filters import Filter
from aiogram.types import Message

from data.requests import get_admins


class IsAdmin(Filter):
    async def __call__(self, message: Message):
        ADMIN_USER_IDS = await get_admins()
        return message.from_user.id in ADMIN_USER_IDS