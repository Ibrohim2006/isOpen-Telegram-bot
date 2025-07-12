from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pydantic import ValidationError
from datetime import datetime
import pytz
import sqlite3
from app.utils.validation import validate_telegram_username

router = Router()
tz = pytz.timezone("Asia/Tashkent")


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


@router.message(Text("Ish beruvchi"))
async def process_employer(message: Message, state: FSMContext):
    await state.update_data(user_type="Employer")
    await EmployerForm.office.set()
    await message.answer("Iltimos, ofis nomini kiriting:", reply_markup=types.ReplyKeyboardRemove())


@router.message(EmployerForm.office)
async def process_office(message: Message, state: FSMContext):
    await state.update_data(office=message.text)
    await EmployerForm.next()
    await message.answer("Texnologiyani kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@router.message(EmployerForm.technology)
async def process_technology(message: Message, state: FSMContext):
    tech = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(technology=tech)
    await EmployerForm.next()
    await message.answer("Telegram foydalanuvchi nomini kiriting (@ bilan):")


@router.message(EmployerForm.telegram_username)
async def process_employer_telegram(message: Message, state: FSMContext):
    try:
        validated_username = validate_telegram_username(message.text)
        await state.update_data(telegram_username=validated_username)
        await EmployerForm.next()
        await message.answer("Hududni kiriting (yoki 'o'tkazib yuborish' deb yozing):")
    except ValidationError:
        await message.answer(
            "Noto'g'ri Telegram foydalanuvchi nomi. Iltimos, @ bilan boshlanadigan to'g'ri nom kiriting.")


@router.message(EmployerForm.area)
async def process_area(message: Message, state: FSMContext):
    area = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(area=area)
    await EmployerForm.next()
    await message.answer("Mas'ul shaxs nomini kiriting:")


@router.message(EmployerForm.responsible)
async def process_responsible(message: Message, state: FSMContext):
    await state.update_data(responsible=message.text)
    await EmployerForm.next()
    await message.answer("Ariza vaqtini kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@router.message(EmployerForm.application_time)
async def process_application_time(message: Message, state: FSMContext):
    app_time = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(application_time=app_time)
    await EmployerForm.next()
    await message.answer("Ish vaqtini kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@router.message(EmployerForm.working_hours)
async def process_working_hours(message: Message, state: FSMContext):
    hours = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(working_hours=hours)
    await EmployerForm.next()
    await message.answer("Maoshni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@router.message(EmployerForm.salary)
async def process_salary(message: Message, state: FSMContext):
    salary = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(salary=salary)
    await EmployerForm.next()
    await message.answer("Qo'shimcha ma'lumotlarni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@router.message(EmployerForm.additional)
async def process_additional(message: Message, state: FSMContext):
    additional = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(additional=additional)

    data = await state.get_data()
    now = datetime.now(tz).isoformat()

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''INSERT INTO employers (
        office, technology, telegram_username, area, responsible, 
        application_time, working_hours, salary, additional, 
        is_sent, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (
                  data['office'], data['technology'], data['telegram_username'],
                  data['area'], data['responsible'], data['application_time'],
                  data['working_hours'], data['salary'], data['additional'],
                  False, now, now
              ))
    conn.commit()
    conn.close()

    await state.clear()
    await message.answer("Ish beruvchi sifatida ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")