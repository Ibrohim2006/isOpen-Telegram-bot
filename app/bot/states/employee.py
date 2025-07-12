from aiogram.fsm.state import State, StatesGroup


class EmployeeForm(StatesGroup):
    full_name = State()
    age = State()
    technology = State()
    phone_number = State()
    telegram_username = State()
    area = State()
    price = State()
    profession = State()
    application_time = State()
    purpose = State()
