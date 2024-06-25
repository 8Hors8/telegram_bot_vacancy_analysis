from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher


async def start(message: types.Message):
    await message.answer("Привет! Я бот, который поможет тебе узнать актуальную "
                         "информацию о медианных зарплатах Python-разработчиков. "
                         "\nЯ собираю данные и визуализирую их в наглядных графиках.")


async def help(message: types.Message):
    await message.answer("Помощь")


def register_command_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=["start"]))
    dp.message.register(help, Command(commands=["help"]))
