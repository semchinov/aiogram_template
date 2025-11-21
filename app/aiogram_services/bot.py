# app/aiogram_services/bot.py

from aiogram import Bot

from app.service.logging.logger import (
    logger,
    str_object_is_created,
    START_MODULE_MESSAGE
)
from app.config.settings import settings


MODULE_DESCRIPTION = "This is module for aiogram bot"


bot = Bot(token=settings.BOT_TOKEN)


if __name__ != "__main__":
    logger.info(str_object_is_created(bot))


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(bot))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
