"""
Reply keyboards for the bot.
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Create main menu keyboard.
    """
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="ℹ️ Help"))
    builder.add(KeyboardButton(text="📖 About"))
    builder.adjust(2)
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Choose an option..."
    )
