from aiogram import types
from aiogram.filters.command import CommandStart

from router import router


@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Assalomu alaykum !")