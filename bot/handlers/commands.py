"""
Basic command handlers (start, help).
"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.keyboards.reply import get_main_keyboard


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handler for /start command.
    """
    await message.answer(
        f"👋 Hello, {message.from_user.full_name}!\n\n"
        f"I'm a template bot built with aiogram 3.x.\n"
        f"Use /help to see available commands.",
        reply_markup=get_main_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Handler for /help command.
    """
    help_text = (
        "📚 <b>Available Commands:</b>\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/about - About this bot\n\n"
        "Just send me any text message and I'll echo it back!"
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("about"))
async def cmd_about(message: Message):
    """
    Handler for /about command.
    """
    about_text = (
        "🤖 <b>About this bot:</b>\n\n"
        "This is a template bot built with aiogram 3.x framework.\n"
        "It demonstrates a modular project structure with:\n"
        "• Command handlers\n"
        "• Message handlers\n"
        "• Middlewares\n"
        "• Filters\n"
        "• Keyboards\n"
        "• Configuration management\n\n"
        "Feel free to use this as a starting point for your own bot!"
    )
    await message.answer(about_text, parse_mode="HTML")
