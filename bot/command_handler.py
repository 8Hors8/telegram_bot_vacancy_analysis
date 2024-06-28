import asyncio

from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start(message: types.Message):
    """
    Обрабатывает команду start
    :param message:
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="График на ежемесячной основе", callback_data="button1")],
        [InlineKeyboardButton(text="График с гибким фильтром", callback_data="button2")]
    ])
    await message.answer("Привет! Я бот, который поможет тебе узнать актуальную "
                         "информацию о медианных зарплатах Python-разработчиков. "
                         "\nЯ собираю данные и визуализирую их в наглядных графиках.")
    await asyncio.sleep(1)
    await message.answer("""
Уточните, пожалуйста, какой именно график заработных плат вас интересует?
Мы можем предоставить вам:

1. График медианной заработной платы на ежемесячной основе:
   - Этот график будет отображать динамику изменения медианной заработной платы Python-разработчиков на ежемесячной основе.
   - Он позволит вам отслеживать тенденции рынка труда в течение года.

2. График с гибким фильтром:
    Альтернативно, мы можем построить график, который позволит вам применять различные фильтры, такие как:
    - Framework
    - Уровень опыта (junior, middle, senior)
    - Дату
    - Город  
    Этот вариант даст вам более гибкие возможности для анализа медианной заработной платы Python-разработчиков в соответствии с вашими конкретными потребностями.

Пожалуйста, сообщите, какой из этих вариантов вам будет более полезен. Я буду рад предоставить вам соответствующую информацию и визуализацию.
""",
                         reply_markup=keyboard)


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
