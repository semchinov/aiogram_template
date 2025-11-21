"""
Inline keyboards for the bot.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Create an example inline keyboard.
    """
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="GitHub", url="https://github.com"))
    builder.add(InlineKeyboardButton(text="aiogram Docs", url="https://docs.aiogram.dev"))
    builder.adjust(1)
    
    return builder.as_markup()
