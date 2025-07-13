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
    except ValueError as e:
        await message.answer(f"Noto'g'ri ism.Misol: Aliyev Vali")


@employee_router.message(EmployeeForm.age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
        if not 16 <= age <= 70:
            await message.answer("❌ Yosh noto'g'ri!\nYosh 16 dan 70 gacha bo'lishi kerak.")
            return
        await state.update_data(age=age)
        await state.set_state(EmployeeForm.technology)
        await message.answer("Texnologiyani kiriting:")
    except ValueError:
        error_msg = (
            "❌ Noto'g'ri format!\n\n"
            "Yosh faqat raqamlarda ko'rsatilishi kerak.\n"
            "Misol uchun: 25"
        )
        await message.answer(error_msg)


@employee_router.message(EmployeeForm.technology)
async def process_technology(message: Message, state: FSMContext):
    await state.update_data(technology=message.text)
    await state.set_state(EmployeeForm.phone_number)
    await message.answer("Telefon raqamingizni kiriting:")


@employee_router.message(EmployeeForm.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    try:
        validated_phone = validate_phone_number(message.text)
        await state.update_data(phone_number=validated_phone)

        username = message.from_user.username
        await state.update_data(telegram_username=f"@{username}" if username else None)

        await state.set_state(EmployeeForm.area)
        await message.answer("Hududni kiriting:")
    except ValueError as e:
        await message.answer(f"Noto'g'ri telefon raqami formati.Misol uchun +998992344556")


@employee_router.message(EmployeeForm.area)
async def process_area(message: Message, state: FSMContext):
    await state.update_data(area=message.text)
    await state.set_state(EmployeeForm.price)
    await message.answer("Maoshni kiriting:")


@employee_router.message(EmployeeForm.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(EmployeeForm.profession)
    await message.answer("Kasbni kiriting:")


@employee_router.message(EmployeeForm.profession)
async def process_profession(message: Message, state: FSMContext):
    await state.update_data(profession=message.text)
    await state.set_state(EmployeeForm.application_time)
    await message.answer("Murojaat vaqtini kiriting:")


@employee_router.message(EmployeeForm.application_time)
async def process_application_time(message: Message, state: FSMContext):
    await state.update_data(application_time=message.text)
    await state.set_state(EmployeeForm.purpose)
    await message.answer("Maqsadni kiriting:")


@employee_router.message(EmployeeForm.purpose)
async def process_purpose(message: Message, state: FSMContext):
    await state.update_data(purpose=message.text)

    db = None
    try:
        data = await state.get_data()
        employee_data = EmployeeModel(**data)

        db = next(get_db())
        saved_employee = await save_employee_to_db(db, employee_data)

        response_message = (
            "✅ Ishchi sifatida ro'yxatdan o'tish muvaffaqiyatli yakunlandi!\n\n"
            "📋 Sizning ma'lumotlaringiz:\n"
            f"👤 To'liq ism: {saved_employee.full_name}\n"
            f"🎂 Yosh: {saved_employee.age}\n"
            f"💻 Texnologiya: {saved_employee.technology}\n"
            f"📞 Telefon: {saved_employee.phone_number}\n"
            f"🔗 Telegram: {saved_employee.telegram_username}\n"
            f"🌐 Hudud: {saved_employee.area}\n"
            f"💰 Maosh: {saved_employee.price}\n"
            f"🛠 Kasb: {saved_employee.profession}\n"
            f"⏰ Murojaat vaqti: {saved_employee.application_time}\n"
            f"🎯 Maqsad: {saved_employee.purpose}\n\n"
            "Tez orada siz bilan bog'lanamiz!"
        )

        await state.clear()
        await message.answer(response_message)
    except ValidationError as e:
        await message.answer(f"❌ Ma'lumotlarda xatolik: {str(e)}")
    except Exception as e:
        logger.error(f"Error saving employee: {str(e)}", exc_info=True)
        await message.answer("❌ Texnik xatolik yuz berdi. Iltimos, keyinroq urunib ko'ring.")
    finally:
        if db is not None:
            db.close()
