from aiogram import types
from aiogram import Dispatcher
from pprint import pprint


async def filter_message_handler(message: types.Message):
    pass

async def message_handler(message: types.Message):
    """
    Обрабатывает входящие сообщения и отправляет ответ.

    :param message: (types.Message): Объект сообщения,
     содержащий информацию о полученном сообщении.
    """
    await message.answer(f'вы вели {message.text}')


def register_message_handlers(dp: Dispatcher):
    """
    Регистрирует обработчики сообщений с предоставленным Dispatcher.

    Эта функция настраивает необходимые обработчики сообщений для обработки входящих сообщений.
    Она регистрирует функцию `message_hendler` для обработки входящих сообщений.

    Аргументы:
    :param dp:dp (Dispatcher) Экземпляр Dispatcher, с которым нужно зарегистрировать обработчики
    """
    dp.message.register(filter_message_handler)
    dp.message.register(message_handler)