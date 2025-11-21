# app/aiogram_services/middlewares/db_session.py

from __future__ import annotations

from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.database.database import get_session
from app.service.logging.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created,
)


MODULE_DESCRIPTION = ("This module provides a middleware for managing database sessions in an asynchronous context using SQLAlchemy."
                      "Like Dependency Injection in FastAPI, it ensures that each request has a dedicated database session.")


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory=get_session):

        logger.debug("Initializing DbSessionMiddleware")

        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:

        logger.debug(f"DbSessionMiddleware called with event: {event}")

        async with self.session_factory() as session:  # type: AsyncSession
            data["db"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(DbSessionMiddleware()))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
