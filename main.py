"""
Main bot entry point.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from bot.handlers import commands, messages
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.utils.logger import setup_logger


logger = logging.getLogger(__name__)


async def main():
    """
    Main function to start the bot.
    """
    # Setup logging
    setup_logger()
    logger.info("Starting bot...")
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher()
    
    # Register middlewares
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    
    # Register routers
    dp.include_router(commands.router)
    dp.include_router(messages.router)
    
    # Log admin IDs
    if settings.admin_ids:
        logger.info(f"Admin IDs: {settings.admin_ids}")
    else:
        logger.warning("No admin IDs configured!")
    
    # Start polling
    try:
        logger.info("Bot started successfully!")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user")
