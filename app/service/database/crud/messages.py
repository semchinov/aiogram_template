# app/services/database/crud/messages.py

from app.logger.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created,
)
from app.services.database.models import Message as DatabaseMessage
from app.aiogram_services.services.utils import build_message_link, strip_aiogram_defaults
from app.config.settings import settings

import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from datetime import datetime
from datetime import timedelta
from aiogram.types import Message as AiogramMessage


MODULE_DESCRIPTION = "This module stores crud functions for messages in the database."


async def create_message(db: AsyncSession, message: AiogramMessage) -> DatabaseMessage:
    """
    Create a new message in the database from an Aiogram Message object.

    Parameters:
        db (AsyncSession): The database session.
        message (AiogramMessage): The message to be saved.

    Returns:
        DatabaseMessage: The created message object.
    """

    logger.debug("Creating new message in database")

    payload =  message.model_dump(
        by_alias=True,
        mode="json",
        exclude_none=True,
        exclude_defaults=True,
        exclude_unset=True,
    )

    payload = strip_aiogram_defaults(payload)

    str_json_data = json.dumps(payload, ensure_ascii=False)

    message_link: str = build_message_link(message)

    logger.debug(f"JSON data: {str_json_data}")

    reply_id = message.reply_to_message.message_id if message.reply_to_message else None
    logger.debug(f"Reply to message id: {reply_id}")

    new_message = DatabaseMessage(
        id=message.message_id,
        chat_id=message.chat.id,
        from_user_id=message.from_user.id,
        reply_to_message=reply_id,
        text=message.text,
        message_link=message_link,
        str_json_data=str_json_data,
    )

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return new_message


async def fetch_context_messages(db: AsyncSession, msg: DatabaseMessage) -> list[DatabaseMessage]:
    """Fetch context messages for a given message.

    The function builds a context chain using reply messages, author's recent messages,
    or recent chat messages according to configured limits. Returned list is ordered
    from older to newer and always ends with the original message.
    """

    logger.debug(f"Fetching context for message id={msg.id}")

    reloaded_msg = await get_message_by_id(db, msg.id)
    if reloaded_msg is not None:
        msg = reloaded_msg

    chain: list[DatabaseMessage] = []
    current = msg
    # Build reply chain
    while current.reply_to_message:
        prev = await get_message_by_id(db, current.reply_to_message)
        if prev is None:
            break
        chain.append(prev)
        current = prev

    chain.reverse()
    if chain:
        chain.append(msg)
        limit = settings.LENGTH_OF_REPLY_CHAIN_LIMIT
        if len(chain) > limit:
            chain = chain[:2] + chain[-(limit - 2):]
        logger.debug(f"Reply chain length: {len(chain)}")
        return chain

    # No reply chain, collect author's recent messages
    time_from = msg.created_at - timedelta(minutes=settings.TIME_OF_LAST_MESSAGES_LIMIT_MINUTES)
    stmt = (
        select(DatabaseMessage)
        .where(
            DatabaseMessage.chat_id == msg.chat_id,
            DatabaseMessage.from_user_id == msg.from_user_id,
            DatabaseMessage.created_at >= time_from,
            DatabaseMessage.created_at < msg.created_at,
        )
        .options(selectinload(DatabaseMessage.theme))
        .order_by(DatabaseMessage.created_at.desc())
        .limit(settings.LENGTH_OF_AUTHOR_CHAIN_LIMIT)
    )
    result = await db.execute(stmt)
    author_msgs = list(result.scalars().all())
    author_msgs.reverse()
    if author_msgs:
        author_msgs.append(msg)
        logger.debug(f"Author chain length: {len(author_msgs)}")
        return author_msgs

    # Fallback: recent chat messages
    stmt = (
        select(DatabaseMessage)
        .where(
            DatabaseMessage.chat_id == msg.chat_id,
            DatabaseMessage.created_at >= time_from,
            DatabaseMessage.created_at < msg.created_at,
        )
        .options(selectinload(DatabaseMessage.theme))
        .order_by(DatabaseMessage.created_at.desc())
        .limit(settings.LENGTH_OF_LAST_MESSAGES_CHAIN_LIMIT)
    )
    result = await db.execute(stmt)
    chat_msgs = list(result.scalars().all())
    chat_msgs.reverse()
    chat_msgs.append(msg)
    logger.debug(f"Chat chain length: {len(chat_msgs)}")
    return chat_msgs


async def get_message_by_id(db: AsyncSession, message_id: int) -> DatabaseMessage | None:
    """
    Retrieve a message from the database by its ID.

    Parameters:
        db (AsyncSession): The database session.
        message_id (int): The ID of the message to retrieve.

    Returns:
        DatabaseMessage | None: The message object if found, otherwise None.
    """

    logger.debug(f"Retrieving message by ID from db: {message_id}")

    stmt = select(DatabaseMessage).where(DatabaseMessage.id == message_id).options(selectinload(DatabaseMessage.theme))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def list_messages(
    db: AsyncSession,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> list[DatabaseMessage]:
    """
    List all messages in the database.

    Parameters:
        db (AsyncSession): The database session.

    Returns:
        list[DatabaseMessage]: A list of all messages.
    """

    logger.debug("Listing all messages from database")

    stmt = select(DatabaseMessage).order_by(DatabaseMessage.created_at.desc())
    if start_time is not None:
        stmt = stmt.where(DatabaseMessage.created_at >= start_time)
    if end_time is not None:
        stmt = stmt.where(DatabaseMessage.created_at <= end_time)

    result = await db.execute(stmt)
    messages = list(result.scalars().all())

    logger.debug(f"Found {len(messages)} messages")

    return messages


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(create_message))
    logger.info(str_object_is_created(fetch_context_messages))
    logger.info(str_object_is_created(get_message_by_id))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
