from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from .register_handlers import register_all_handlers
class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)


    async def run(self):
        register_all_handlers(self.dp)
        await self.dp.start_polling(self.bot)

if __name__ == '__main__':
    pass