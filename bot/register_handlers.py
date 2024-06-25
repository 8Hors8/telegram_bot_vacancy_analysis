from aiogram import Dispatcher
from .command_handler import register_command_handlers

def register_all_handlers(dp: Dispatcher):
    register_command_handlers(dp)