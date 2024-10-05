
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply("Welcome! How can I help you?")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
