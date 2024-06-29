# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.filters.callback_data import CallbackData
#
# class InlineButtonCallback(CallbackData, prefix="button"):
#     action: str
#
# def get_initial_inline_kb():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Опция 1", callback_data=InlineButtonCallback(action="option1"))
#     builder.button(text="Опция 2", callback_data=InlineButtonCallback(action="option2"))
#     builder.button(text="Далее", callback_data=InlineButtonCallback(action="next"))
#     return builder.as_markup()
#
# def get_next_inline_kb():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Опция 3", callback_data=InlineButtonCallback(action="option3"))
#     builder.button(text="Опция 4", callback_data=InlineButtonCallback(action="option4"))
#     builder.button(text="Назад", callback_data=InlineButtonCallback(action="back"))
#     return builder.as_markup()