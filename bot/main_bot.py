from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.storage.memory import MemoryStorage

class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(storage=MemoryStorage())



    async def run(self):
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    pass


