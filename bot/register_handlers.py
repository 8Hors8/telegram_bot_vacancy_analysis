from aiogram import Dispatcher
from .command_handler import register_command_handlers
from .message_handler import register_message_handlers
from .callback_handler import register_callback_handlers


def register_all_handlers(dp: Dispatcher):
    """
    Регистрирует все обработчики сообщений, команд и кнопок.

    Эта функция вызывает другие функции для регистрации обработчиков сообщений,
    команд и кнопок с предоставленным Dispatcher.
    Она обеспечивает централизованную точку для регистрации всех необходимых обработчиков.

    :param dp:dp (Dispatcher): Экземпляр Dispatcher,
     с которым нужно зарегистрировать обработчики.
    """
    register_command_handlers(dp)
    register_message_handlers(dp)
    register_callback_handlers(dp)
