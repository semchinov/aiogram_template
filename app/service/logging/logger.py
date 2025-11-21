# app/logging/logger.py

import logging
import sys
from loguru import logger
from typing import Any


MODULE_DESCRIPTION = "This module stores logger settings and configurations"


START_MODULE_MESSAGE = "You have launched the module "


class InterceptHandler(logging.Handler):
    """
    This class intercepts logging messages and
    redirects them from logging logger (standard
    python) to loguru logger.
    """
    def emit(self, record: logging.LogRecord) -> None:
        # logging levels are INFO DEBUG and so on
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """
    This function sets up the logging configuration for the application.
    """

    # delete default sink by loguru
    logger.remove()

    fmt_console = (
        "<bold><fg #9cdcfe>{time:YYYY-MM-DD HH:mm:ss.SSS}</fg #9cdcfe></bold> "
        "| <bold><lvl>{level: <7}</lvl></bold> "
        "| <fg #dcdcaa>{name}</fg #dcdcaa>:"
        "<fg #ce9178>{function}</fg #ce9178>:"
        "<fg #b5cea8>{line}</fg #b5cea8> "
        "| <dim>{process.name}</dim> "
        "- <bold><lvl>{message}</lvl></bold>"
    )

    logger.add(
        sys.stdout,
        level="DEBUG",
        filter=lambda r: r["level"].no < logger.level("INFO").no,
        format=fmt_console,
        enqueue=True,
    )

    logger.add(
        sys.stdout,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
        colorize=True,
        format=fmt_console,
    )

    # send ALL to InterceptHandler
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    AIROUTERS_LOGGERS = (
        "aiogram",
        "aiogram.bot",
        "aiogram.dispatcher",
        "aiogram.fsm",
        "aiogram.event",
        "aiogram.bot.api",
        "aiohttp",
        "aiohttp.client",
        "aiohttp.server",
    )

    for name in AIROUTERS_LOGGERS:
        lg = logging.getLogger(name)
        lg.handlers.clear()
        lg.propagate = True
        lg.setLevel(logging.DEBUG)


# Function for dynamic logger information (Python module info)
def str_object_is_created(created_object: Any) -> str:
    """
        Function for making string with description of creation of object
            Parameters:
                created_object: creation of this object we should describe
            Returns:
                str: description of creation of object
    """
    return f"Object {created_object} is created"


setup_logging()


def main():
    logger.info("Logging has been set up successfully.")
    logger.debug("Debugging information is available.")
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info("Module description: " + MODULE_DESCRIPTION)
    logger.info(str_object_is_created(logger))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
