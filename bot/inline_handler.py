from aiogram import types
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from .inline_buttons import InlineButtonCallback, get_initial_inline_kb, get_next_inline_kb


async def inline_button_handler(callback_query: types.CallbackQuery, callback_data: InlineButtonCallback,
                                state: FSMContext):
    if callback_data.action == "next":
        await callback_query.message.edit_text("Выберите опцию:", reply_markup=get_next_inline_kb())
    elif callback_data.action == "back":
        await callback_query.message.edit_text("Выберите опцию:", reply_markup=get_initial_inline_kb())
    elif callback_data.action == "option1":
        await callback_query.message.answer("Вы выбрали Опцию 1")
    elif callback_data.action == "option2":
        await callback_query.message.answer("Вы выбрали Опцию 2")
    elif callback_data.action == "option3":
        await callback_query.message.answer("Вы выбрали Опцию 3")
    elif callback_data.action == "option4":
        await callback_query.message.answer("Вы выбрали Опцию 4")
    await callback_query.answer()


def register_inline_handlers(dp: Dispatcher):
    dp.callback_query.register(inline_button_handler, InlineButtonCallback.filter())
