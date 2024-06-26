from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FilterForm(StatesGroup):
    """
    Состояния для формы фильтра.

    Этот класс определяет состояния, в которых может
    находиться пользователь в процессе взаимодействия
    с формой фильтра в боте. Каждое состояние соответствует
    определенному шагу ввода информации.

    Состояния:
    - waiting_for_role: Ожидание выбора роли
    (например, junior, middle, senior).
    - waiting_for_city: Ожидание ввода города.
    """
    waiting_for_role = State()
    waiting_for_city = State()


class FilterFreeForm(StatesGroup):
    """
   Состояния для формы фильтра.

   Этот класс определяет состояния, в которых может
   находиться пользователь в процессе взаимодействия
   с формой фильтра в боте. Каждое состояние соответствует
   определенному шагу ввода информации.

   Состояния:
   - waiting_for_filter: Ожидание ввода фильтра
   (например, [django, middle, senior]).
   -  waiting_for_date Ожидание ввода даты
   (например, ['дата от','дата до'] пример ['2024-03', '2024-04'])
   - waiting_for_city: Ожидание ввода города или региона.
   """
    waiting_for_filter = State()
    waiting_for_date = State()
    waiting_for_city = State()


async def button1_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    r_kb = [
        [types.KeyboardButton(text="Python Developer")],
        [types.KeyboardButton(text="Django")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=r_kb, resize_keyboard=True)

    await callback_query.message.answer("Введите параметр фильтрации:", reply_markup=keyboard)
    await state.set_state(FilterForm.waiting_for_role)


async def button2_callback_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("""
    Введите параметры для фильтрации:
    Вы можете указать несколько параметров через запятую, например (django, middle, senior).
    Также можно указать несколько фреймворков.
    Параметр "python" формирует график медианной зарплаты по всем направлениям и уровням разработчиков.
    """)
    await state.set_state(FilterFreeForm.waiting_for_filter)


def register_callback_handlers(dp: Dispatcher):
    """
    Регистрирует обработчики inlin button с предоставленным Dispatcher.

    Эта функция настраивает необходимые обработчики сообщений для обработки входящих сообщений.
    Она регистрирует функцию `message_hendler` для обработки входящих сообщений.

    Аргументы:
    :param dp:dp (Dispatcher) Экземпляр Dispatcher, с которым нужно зарегистрировать обработчики
    """
    dp.callback_query.register(button1_callback_handler, F.data == "button1")
    dp.callback_query.register(button2_callback_handler, F.data == "button2")
