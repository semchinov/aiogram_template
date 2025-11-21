# app/services/database/crud/notification_rules.py

from app.logger.logger import (
    logger,
    START_MODULE_MESSAGE,
    str_object_is_created,
)
from app.services.database.models import (
    NotificationRule,
    MessageEmotionEnum,
    MessageTheme,
    Message,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import UUID4


MODULE_DESCRIPTION = "CRUD functions for notification rules in the database."


async def list_rules(db: AsyncSession) -> list[NotificationRule]:
    """List all notification rules."""

    logger.debug("Listing notification rules from database")

    stmt = select(NotificationRule)
    result = await db.execute(stmt)
    rules = list(result.scalars().all())

    logger.debug(f"Found {len(rules)} notification rules")

    return rules


async def get_rule_by_theme_and_emotion(
    db: AsyncSession,
    message_theme_uuid: UUID4,
    emotion: MessageEmotionEnum,
) -> NotificationRule | None:
    """Return the notification rule for the given theme and emotion, if any."""

    logger.debug(
        "Fetching notification rule for theme %s and emotion %s", message_theme_uuid, emotion
    )

    stmt = select(NotificationRule).where(
        NotificationRule.message_theme_uuid == message_theme_uuid,
        NotificationRule.emotion == emotion,
    )
    result = await db.execute(stmt)
    rule = result.scalar_one_or_none()

    if rule is None:
        logger.debug(
            "Notification rule for theme %s and emotion %s not found", message_theme_uuid, emotion
        )
    else:
        logger.debug(
            "Notification rule %s found for theme %s and emotion %s",
            rule.uuid,
            message_theme_uuid,
            emotion,
        )

    return rule


async def get_or_create_rule(
    db: AsyncSession,
    message_theme_uuid: UUID4,
    emotion: MessageEmotionEnum,
) -> NotificationRule:
    """Return an existing notification rule or create a new one if it does not exist."""

    logger.debug(
        "Getting or creating notification rule for theme %s and emotion %s",
        message_theme_uuid,
        emotion,
    )

    rule = await get_rule_by_theme_and_emotion(db, message_theme_uuid, emotion)

    if rule is None:
        logger.debug(
            "Notification rule missing for theme %s and emotion %s. Creating a new one.",
            message_theme_uuid,
            emotion,
        )
        rule = await create_rule(db, message_theme_uuid, emotion)
    else:
        logger.debug(
            "Notification rule %s already exists for theme %s and emotion %s",
            rule.uuid,
            message_theme_uuid,
            emotion,
        )

    return rule


async def rule_exists_for_current_theme_and_emotion(
    db: AsyncSession,
    emotion: MessageEmotionEnum,
    message_theme_uuid: UUID4 | None = None,
    message_theme: MessageTheme | None = None
) -> bool:
    """Check if an active notification rule exists for the given theme and emotion."""

    logger.debug("Start function rule_exists_for_current_theme_and_emotion")

    if message_theme_uuid is None:
        if message_theme is not None:
            message_theme_uuid = message_theme.uuid
        else:
            raise ValueError("Either message_theme_uuid or message_theme must be provided")

    rule = await get_rule_by_theme_and_emotion(db, message_theme_uuid, emotion)

    if rule and rule.active:
        logger.debug(
            "Active notification rule %s found for theme %s and emotion %s",
            rule.uuid,
            message_theme_uuid,
            emotion,
        )
        return True

    logger.debug(
        "Active notification rule not found for theme %s and emotion %s",
        message_theme_uuid,
        emotion,
    )

    return False


async def rule_exists_for_current_message(
    db: AsyncSession,
    message: Message
) -> bool:
    """Check if a notification rule exists for the given message's theme and emotion."""

    logger.debug("Start function rule_exists_for_current_message")

    if message.message_theme_uuid is None or message.emotion is None:
        logger.error("Message must have both message_theme_uuid and emotion set")
        return False

    return await rule_exists_for_current_theme_and_emotion(
        db,
        emotion=message.emotion,
        message_theme_uuid=message.message_theme_uuid
    )


async def create_rule(
    db: AsyncSession,
    message_theme_uuid: UUID4,
    emotion: MessageEmotionEnum,
) -> NotificationRule:
    """Create a new notification rule."""

    logger.debug(
        f"Creating notification rule for theme {message_theme_uuid} and emotion {emotion}"
    )

    rule = NotificationRule(
        message_theme_uuid=message_theme_uuid,
        emotion=emotion,
        active=True,
    )

    db.add(rule)
    await db.commit()
    await db.refresh(rule)

    logger.info(f"Created notification rule {rule.uuid}")

    return rule


async def toggle_rule(db: AsyncSession, rule: NotificationRule) -> NotificationRule:
    """Toggle the active state of a notification rule."""

    logger.debug(f"Toggling notification rule {rule.uuid}")

    rule.active = not rule.active

    db.add(rule)
    await db.commit()
    await db.refresh(rule)

    logger.info(f"Notification rule {rule.uuid} active={rule.active}")

    return rule


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(NotificationRule))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
