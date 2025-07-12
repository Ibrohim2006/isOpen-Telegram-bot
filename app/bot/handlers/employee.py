from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError
from datetime import datetime
import pytz

from app.bot.states.employee import EmployeeForm
from app.database.models import Employee
from app.database.base import get_db
from app.database.schemas.employee import EmployeeModel
from app.utils.validation import (
    validate_full_name,
    validate_phone_number,
    validate_telegram_username
)
from app.core.logger import logger

employee_router = Router()
tz = pytz.timezone("Asia/Tashkent")


async def save_employee_to_db(db, employee_data: EmployeeModel):
    employee = Employee(
        full_name=employee_data.full_name,
        age=employee_data.age,
        technology=employee_data.technology,
        phone_number=employee_data.phone_number,
        telegram_username=employee_data.telegram_username,
        area=employee_data.area,
        price=employee_data.price,
        profession=employee_data.profession,
        application_time=employee_data.application_time,
        purpose=employee_data.purpose,
        is_sent=False,
        created_at=datetime.now(tz),
        updated_at=datetime.now(tz)
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@employee_router.message(F.text == "Ishchi")
async def process_employee(message: Message, state: FSMContext):
    await state.update_data(user_type="Employee")
    await state.set_state(EmployeeForm.full_name)
    await message.answer(
        "Iltimos, to'liq ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )


@employee_router.message(EmployeeForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    try:
        validated_name = validate_full_name(message.text)
        await state.update_data(full_name=validated_name)
        await state.set_state(EmployeeForm.age)
        await message.answer("Yoshingizni kiriting:")
    except ValidationError as e:
        await message.answer(f"Noto'g'ri ism: {str(e)}")


@employee_router.message(EmployeeForm.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if not 1 <= age <= 70:
            raise ValueError("Yosh 1 dan 70 gacha bo'lishi kerak")
        await state.update_data(age=age)
        await state.set_state(EmployeeForm.technology)
        await message.answer("Texnologiyani kiriting (yoki 'o'tkazib yuborish' deb yozing):")
    except ValueError as e:
        await message.answer(f"Noto'g'ri yosh: {str(e)}")


@employee_router.message(EmployeeForm.technology)
async def process_technology(message: Message, state: FSMContext):
    tech = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(technology=tech)
    await state.set_state(EmployeeForm.phone_number)
    await message.answer("Telefon raqamingizni kiriting:")


@employee_router.message(EmployeeForm.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    try:
        validated_phone = validate_phone_number(message.text)
        await state.update_data(phone_number=validated_phone)
        await state.set_state(EmployeeForm.telegram_username)
        await message.answer("Telegram foydalanuvchi nomini kiriting (@ bilan):")
    except ValidationError as e:
        await message.answer(f"Noto'g'ri telefon raqami: {str(e)}")


@employee_router.message(EmployeeForm.telegram_username)
async def process_telegram_username(message: Message, state: FSMContext):
    try:
        validated_username = validate_telegram_username(message.text)
        await state.update_data(telegram_username=validated_username)
        await state.set_state(EmployeeForm.area)
        await message.answer("Hududni kiriting (yoki 'o'tkazib yuborish' deb yozing):")
    except ValidationError as e:
        await message.answer(f"Noto'g'ri Telegram nomi: {str(e)}")


@employee_router.message(EmployeeForm.area)
async def process_area(message: Message, state: FSMContext):
    area = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(area=area)
    await state.set_state(EmployeeForm.price)
    await message.answer("Narxni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employee_router.message(EmployeeForm.price)
async def process_price(message: Message, state: FSMContext):
    price = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(price=price)
    await state.set_state(EmployeeForm.profession)
    await message.answer("Kasbni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employee_router.message(EmployeeForm.profession)
async def process_profession(message: Message, state: FSMContext):
    profession = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(profession=profession)
    await state.set_state(EmployeeForm.application_time)
    await message.answer("Ariza vaqtini kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employee_router.message(EmployeeForm.application_time)
async def process_application_time(message: Message, state: FSMContext):
    app_time = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(application_time=app_time)
    await state.set_state(EmployeeForm.purpose)
    await message.answer("Maqsadni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employee_router.message(EmployeeForm.purpose)
async def process_purpose(message: Message, state: FSMContext):
    purpose = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(purpose=purpose)

    db = None
    try:
        data = await state.get_data()
        employee_data = EmployeeModel(**data)

        db = next(get_db())
        await save_employee_to_db(db, employee_data)

        await state.clear()
        await message.answer("✅ Ishchi sifatida ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")
    except ValidationError as e:
        await message.answer(f"❌ Ma'lumotlarda xatolik: {str(e)}")
    except Exception as e:
        logger.error(f"Error saving employee: {str(e)}", exc_info=True)
        await message.answer("❌ Texnik xatolik yuz berdi. Iltimos, keyinroq urunib ko'ring.")
    finally:
        if db is not None:
            db.close()
