"""
Throttling middleware to prevent spam.
"""
import logging
import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Message

from config import settings


logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple throttling middleware.
    Prevents users from sending messages too frequently.
    """
    
    def __init__(self, rate_limit: float = None):
        self.rate_limit = rate_limit or settings.rate_limit
        self.user_timestamps: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        
        if user and isinstance(event, Message):
            current_time = time.time()
            user_id = user.id
            
            if user_id in self.user_timestamps:
                time_passed = current_time - self.user_timestamps[user_id]
                
                if time_passed < self.rate_limit:
                    logger.warning(f"User {user_id} is being throttled")
                    await event.answer("⚠️ Please don't spam! Wait a moment.")
                    return
            
            self.user_timestamps[user_id] = current_time
        
        return await handler(event, data)
