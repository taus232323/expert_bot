from aiogram.filters import Filter
from aiogram.types import Message

from settings import SUPER_ADMIN_USER_IDS


class IsSuperAdmin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in SUPER_ADMIN_USER_IDS
    