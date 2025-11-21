"""
Custom filters for the bot.
"""
from aiogram.filters import Filter
from aiogram.types import Message

from config import settings


class IsAdminFilter(Filter):
    """
    Filter to check if user is admin.
    """
    
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in settings.admin_ids
