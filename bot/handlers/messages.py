"""
Message handlers for text and other content.
"""
from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text)
async def echo_message(message: Message):
    """
    Echo back any text message.
    """
    await message.answer(
        f"🔄 You said: {message.text}"
    )


@router.message(F.photo)
async def handle_photo(message: Message):
    """
    Handle photo messages.
    """
    await message.answer(
        "📷 Nice photo! I received your image."
    )


@router.message(F.document)
async def handle_document(message: Message):
    """
    Handle document messages.
    """
    file_name = message.document.file_name or "unnamed file"
    await message.answer(
        f"📄 Document received: {file_name}"
    )


@router.message(F.sticker)
async def handle_sticker(message: Message):
    """
    Handle sticker messages.
    """
    await message.answer(
        "😊 Cool sticker!"
    )
