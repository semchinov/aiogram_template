# app/aiogram_services/main.py

from app.aiogram_services.bot import bot
from app.service.logging.logger import (
    logger,
    str_object_is_created,
    START_MODULE_MESSAGE,
)
from app.aiogram_services.routers import (
    start_router,
)

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


MODULE_DESCRIPTION = "This is main module for aiogram. Functions to start aiogram bot and run FastAPI app."


storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_router(start_router)


async def dp_task() -> None:
    """
    Start polling in a controlled way:
    - resolve allowed updates,
    - close bot session on shutdown.
    """
    allowed_updates = dp.resolve_used_update_types()
    logger.info(f"Starting polling. allowed_updates={allowed_updates}")
    try:
        await dp.start_polling(bot, allowed_updates=allowed_updates)
    finally:
        try:
            await bot.session.close()
        except Exception as e:
            logger.error(f"Failed to close bot session: {e}")
        logger.info("Bot stopped.")



def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(dp))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
