from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher


async def start(message: types.Message):
    """
    Обрабатывает команду start
    :param message:
    """
    await message.answer("Привет! Я бот, который поможет тебе узнать актуальную "
                         "информацию о медианных зарплатах Python-разработчиков. "
                         "\nЯ собираю данные и визуализирую их в наглядных графиках.")


async def help(message: types.Message):
    """
    Обрабатывает команду help
    :param message:
    """
    await message.answer("Помощь")


def register_command_handlers(dp: Dispatcher):
    """
    Регистрирует обработчики команд в предоставленном Dispatcher.
    :param dp:dp (Dispatcher): Экземпляр Dispatcher,
     с которым нужно зарегистрировать обработчики команд.
    """
    dp.message.register(start, Command(commands=["start"]))
    dp.message.register(help, Command(commands=["help"]))
