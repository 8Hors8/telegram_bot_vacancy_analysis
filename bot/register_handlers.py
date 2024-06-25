from aiogram import Dispatcher


def register_all_handlers(dp: Dispatcher):
    register_common_handlers(dp)
    register_inline_handlers(dp)