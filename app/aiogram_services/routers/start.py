# app/aiogram_services/routers/start.py

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.service.logging.logger import (
    logger,
    str_object_is_created,
    START_MODULE_MESSAGE,
)


MODULE_DESCRIPTION = "This module stores router for aiogram - registration."


start_router: Router = Router(name="Start")


@start_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):

    logger.debug("Start function 'start_command'. message: {message}, state: {state}")

    await message.answer("Seems you shouldn't be here")
    # await state.set_state(SomeState.some_state)  # TODO: Replace SomeState and some_state with actual state and state name


def main():
    logger.info(START_MODULE_MESSAGE + str(__file__))
    logger.info(MODULE_DESCRIPTION)
    logger.info(str_object_is_created(start_router))


if __name__ != "__main__":
    main()


if __name__ == "__main__":
    main()
