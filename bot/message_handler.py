import re
from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile
from building_salary_schedules import monthly_salary_plot, delete_graph
import constants


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


async def filter_criteria_handler(message: types.Message, state: FSMContext):
    if message.text in ["Python Developer", "Django"]:
        await state.update_data(role=message.text)

        r_kb = [
            [types.KeyboardButton(text="Москва")],
            [types.KeyboardButton(text="Новосибирск")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=r_kb, resize_keyboard=True)
        await message.answer("Укажите город:", reply_markup=keyboard)
        await state.set_state(FilterForm.waiting_for_city)
    else:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")


async def city_handler(message: types.Message, state: FSMContext):
    if message.text in ["Москва", "Новосибирск"]:
        user_data = await state.get_data()
        role = user_data.get("role")
        city = message.text

        # Очистка клавиатуры
        remove_keyboard = types.ReplyKeyboardRemove()
        await message.answer(f"Вы выбрали: Роль - {role}, Город - {city}",
                             reply_markup=remove_keyboard)
        filter_ = {
            'filter': role.lower(),
            'city': city
        }
        graph_path = await monthly_salary_plot(filter_, str(message.from_user.id))
        photo = FSInputFile(graph_path)
        try:
            await message.answer_photo(photo=photo)
            # Удаляем график после успешной отправки
            delete_graph(graph_path)
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке фото: {e}")
        await state.clear()
    else:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")


async def free_filter_handler(message: types.Message, state: FSMContext):
    workpiece = re.split(r'[,\s;.]+', message.text.lower())
    workpiece_list = [item for item in workpiece if item]
    frame_develop = constants.framework + constants.developer + constants.language
    filter_list = []
    for el in workpiece_list:
        if el in frame_develop:
            if el == 'python':
                filter_list.append('python developer')
            else:
                filter_list.append(el)
        else:
            await message.answer(f'Некорректный параметр {el}')
    if filter_list:
        await state.update_data(filter_list=filter_list)
        await message.answer("""
        Дополнительный параметр: дата.
        Отправьте "pass", чтобы пропустить.
        Формат: дата от, дата до, например, 2024-03, 2024-04
        """)
        await state.set_state(FilterFreeForm.waiting_for_date)
    else:
        await message.answer("""
Извините, но вы не указали ни одного корректного параметра для фильтрации.
Пожалуйста, попробуйте снова и укажите корректные параметры фильтра.
Вы можете указать несколько параметров через запятую, например: (django, middle, senior).
Также вы можете указать несколько фреймворков.
        """)


async def free_date_handler(message: types.Message, state: FSMContext):
    date_workpiece = re.split(r'[,\s;.]+', message.text.lower())
    dates = [item for item in date_workpiece if item]
    pattern = re.compile(r'^\d{4}-\d{2}$')
    notification = """
    Дополнительный параметр: город.
    Отправьте "pass", чтобы пропустить.
    """
    if dates[0] != 'pass':
        warning = 'tru'
        for date in dates:
            if re.match(pattern, date):
                pass
            else:
                warning = ('Вы указали не верную дату.'
                           '\nФормат: дата от, дата до, например, 2024-03, 2024-04')
        if warning == 'tru':
            await state.update_data(dates=dates)
            await message.answer(notification)
            await state.set_state(FilterFreeForm.waiting_for_city)
        else:
            await message.answer(warning)
    else:
        await message.answer(notification)
        await state.set_state(FilterFreeForm.waiting_for_city)


async def stub_message_handler(message: types.Message):
    """
    Заглушка.

    :param message: (types.Message): Объект сообщения,
     содержащий информацию о полученном сообщении.
    """
    await message.answer('Я вас не понимаю')


def register_message_handlers(dp: Dispatcher):
    """
    Регистрирует обработчики сообщений с предоставленным Dispatcher.

    Эта функция настраивает необходимые обработчики сообщений для обработки входящих сообщений.
    Она регистрирует функцию `message_hendler` для обработки входящих сообщений.

    Аргументы:
    :param dp:dp (Dispatcher) Экземпляр Dispatcher, с которым нужно зарегистрировать обработчики
    """

    dp.message.register(filter_criteria_handler, FilterForm.waiting_for_role)
    dp.message.register(city_handler, FilterForm.waiting_for_city)
    dp.message.register(free_filter_handler, FilterFreeForm.waiting_for_filter)
    dp.message.register(free_date_handler, FilterFreeForm.waiting_for_date)

    dp.message.register(stub_message_handler)
