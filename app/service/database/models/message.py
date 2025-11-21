# app/services/database/models/message.py

from sqlmodel import SQLModel, Field, Relationship, Column, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from pydantic import StrictInt, StrictStr, UUID4
from uuid import uuid4
from datetime import datetime

from app.service.logging.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created,
)


MODULE_DESCRIPTION = "This module stores models for SQL. It contains classes for working with the database."


class AsyncBase(AsyncAttrs, SQLModel):
    pass


class Message(AsyncBase, table=True):
    uuid:               UUID4            = Field(default_factory=uuid4, primary_key=True)
    created_at:         datetime         = Field(default_factory=datetime.utcnow)
    id:                 StrictInt        = Field(sa_column=Column(BigInteger, nullable=False))
    chat_id:            StrictInt        = Field(sa_column=Column(BigInteger, nullable=False))
    from_user_id:       StrictInt        = Field(sa_column=Column(BigInteger, nullable=False))
    reply_to_message:   StrictInt | None = Field(default=None, sa_column=Column(BigInteger))
    text:               StrictStr
    message_link:       StrictStr | None = None
    str_json_data:      StrictStr


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(Message))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
