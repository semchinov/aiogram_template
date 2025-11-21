# app/services/database/crud/message_themes.py

from app.logger.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created,
)
from app.services.database.models import MessageTheme as DatabaseMessageTheme
from app.services.llm.schemas import MessageTheme as LangchainMessageTheme

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


MODULE_DESCRIPTION = "This module stores crud functions for messages in the database."


async def list_message_themes(db: AsyncSession) -> list[DatabaseMessageTheme]:
    """
    List all message themes from the database.

    Parameters:
        db (AsyncSession): The database session.

    Returns:
        list[MessageTheme]: A list of all message themes.
    """

    logger.debug("Listing all message themes from database")

    stmt = select(DatabaseMessageTheme).order_by(DatabaseMessageTheme.created_at.desc())
    result = await db.execute(stmt)
    themes = list(result.scalars().all())

    logger.debug(f"Found {len(themes)} message themes")

    return themes


async def list_enabled_message_themes(db: AsyncSession) -> list[DatabaseMessageTheme]:
    """
    List only enabled message themes from the database.

    Parameters:
        db (AsyncSession): The database session.

    Returns:
        list[MessageTheme]: A list of enabled message themes.
    """

    logger.debug("Listing enabled message themes from database")

    stmt = (
        select(DatabaseMessageTheme)
        .where(DatabaseMessageTheme.enable == True)  # noqa: E712
        .order_by(DatabaseMessageTheme.created_at.desc())
    )
    result = await db.execute(stmt)
    themes = list(result.scalars().all())

    logger.debug(f"Found {len(themes)} enabled message themes")

    return themes


async def get_message_theme_by_name(db: AsyncSession, name: str) -> DatabaseMessageTheme | None:
    """
    Get a message theme by its name.

    Parameters:
        db (AsyncSession): The database session.
        name (str): The name of the message theme.

    Returns:
        MessageTheme: The message theme with the specified name, or None if not found.
    """

    logger.debug(f"Getting message theme by name: {name}")

    stmt = select(DatabaseMessageTheme).where(DatabaseMessageTheme.name == name)
    result = await db.execute(stmt)
    theme = result.scalar_one_or_none()

    if theme is None:
        logger.debug(f"Message theme {name} not found")
    else:
        logger.debug(f"Found message theme: {theme}")

    return theme


async def message_theme_exists(db: AsyncSession, name: str) -> bool:
    """
    Check if a message theme exists by its name.

    Parameters:
        db (AsyncSession): The database session.
        name (str): The name of the message theme.

    Returns:
        bool: True if the message theme exists, False otherwise.
    """

    logger.debug(f"Checking if message theme exists by name: {name}")

    message_theme: DatabaseMessageTheme | None = await get_message_theme_by_name(db, name)
    exists: bool = message_theme is not None

    return exists


async def add_new_keywords_to_theme(db: AsyncSession, theme: DatabaseMessageTheme, new_keywords: list[str]) -> DatabaseMessageTheme:
    """
    Add new keywords to a message theme.
    Parameters:
        db (AsyncSession): The database session.
        theme (MessageTheme): The message theme to update.
        new_keywords (list[str]): The new keywords to add.
    Returns:
        MessageTheme: The updated message theme.
    """

    logger.debug(f"Adding new keywords to message theme {theme.name}: {new_keywords}")

    existing_keywords = set(theme.keywords or [])
    updated_keywords = list(existing_keywords.union(new_keywords))
    theme.keywords = updated_keywords

    db.add(theme)
    await db.commit()
    await db.refresh(theme)

    logger.debug(f"Updated message theme: {theme}")

    return theme


async def there_are_less_than_n_different_keywords_in_theme(theme: DatabaseMessageTheme, keywords: list[str], n: int = 3) -> bool:
    """
    Check if there are less than n different keywords in a message theme.
    Parameters:
        db (AsyncSession): The database session.
        theme (MessageTheme): The message theme to check.
        keywords (list[str]): The keywords to compare.
        n (int): The threshold number of different keywords.
    Returns:
        bool: True if there are less than n different keywords, False otherwise.
    """

    logger.debug(f"Checking if there are less than {n} different keywords in theme {theme.name}")

    existing_keywords = set(theme.keywords or [])
    new_keywords = set(keywords)
    different_keywords = new_keywords - existing_keywords

    logger.debug(f"Different keywords: {different_keywords}")

    return len(different_keywords) < n


async def create_message_theme(db: AsyncSession, theme: LangchainMessageTheme) -> DatabaseMessageTheme:
    """
    Create a new message theme in the database.

    Parameters:
        db (AsyncSession): The database session.
        theme (LangchainMessageTheme): The message theme to create.

    Returns:
        DatabaseMessageTheme: The newly created message theme.
    """

    logger.debug(f"Creating new message theme: {theme}")

    new_theme = DatabaseMessageTheme(
        name=theme.name,
        description=theme.description,
        keywords=theme.keywords or [],
    )

    db.add(new_theme)
    await db.commit()
    await db.refresh(new_theme)

    logger.info(f"Created new message theme: {new_theme}")

    return new_theme


async def check_and_create_or_update_theme(db: AsyncSession, theme: LangchainMessageTheme) -> DatabaseMessageTheme:
    """
    Check if a message theme exists by its name, and create it if it does not exist.

    Parameters:
        db (AsyncSession): The database session.
        theme (LangchainMessageTheme): The message theme to check and create.

    Returns:
        DatabaseMessageTheme: The existing or newly created message theme.
    """

    logger.debug(f"Checking and creating message theme if not exists: {theme}")

    if await message_theme_exists(db, theme.name):
        existing_theme: DatabaseMessageTheme = await get_message_theme_by_name(db, theme.name)

        if await there_are_less_than_n_different_keywords_in_theme(existing_theme, theme.keywords or [], n=3):
            existing_theme: DatabaseMessageTheme = await add_new_keywords_to_theme(db, existing_theme, theme.keywords or [])

        return existing_theme

    created_theme: DatabaseMessageTheme =  await create_message_theme(db, theme)

    return created_theme


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(list_message_themes))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
