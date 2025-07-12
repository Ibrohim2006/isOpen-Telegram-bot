from aiogram.fsm.state import State, StatesGroup


class EmployerForm(StatesGroup):
    office = State()
    technology = State()
    telegram_username = State()
    area = State()
    responsible = State()
    application_time = State()
    working_hours = State()
    salary = State()
    additional = State()
