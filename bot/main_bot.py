from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .register_handlers import register_all_handlers
class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(storage=MemoryStorage())

        register_all_handlers(self.dp)
    async def run(self):
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    pass