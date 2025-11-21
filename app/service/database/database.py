# app/services/database/database.py

from app.config.settings import settings
from app.service.logging.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created,
)
from app.service.database.models.message import Message # noqa: F401

import asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlmodel import SQLModel
from typing import AsyncGenerator


MODULE_DESCRIPTION = "This module is used for access to the database"


connect_args: dict = {}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args,
    pool_size=20,
    max_overflow=20,
)


async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """
        Function for initializing the database
    """

    logger.info(f"Connecting to DB: {settings.DATABASE_URL}")

    async with engine.begin() as conn:
        logger.info(str_object_is_created(engine))
        logger.info(str_object_is_created(async_session_factory))
        await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database is successfully connected")
        logger.info(f"Current database: {engine.url}")


def get_session() -> AsyncSession:
    """
        Returns an async session object
    """
    return async_session_factory()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
        Use for dependency injection in FastAPI
    """
    async with async_session_factory() as session:
        yield session


async def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(f"Connecting to DB: {settings.DATABASE_URL}")
    logger.info(str_object_is_created(engine))
    logger.info(str_object_is_created(async_session_factory))
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database is successfully connected")
    logger.info(f"Current database: {engine.url}")


def sync_main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(engine))
    logger.info(str_object_is_created(async_session_factory))


if __name__ != "__main__":
    sync_main()


if __name__ == "__main__":
    asyncio.run(main())
