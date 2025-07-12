from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError
from datetime import datetime
import pytz

from app.bot.states.employer import EmployerForm
from app.database.models import Employer
from app.database.base import get_db
from app.database.schemas.employer import EmployerModel
from app.utils.validation import validate_telegram_username
from app.core.logger import logger

employer_router = Router()
tz = pytz.timezone("Asia/Tashkent")


async def save_employer_to_db(db, employer_data: EmployerModel):
    employer = Employer(
        office=employer_data.office,
        technology=employer_data.technology,
        telegram_username=employer_data.telegram_username,
        area=employer_data.area,
        responsible=employer_data.responsible,
        application_time=employer_data.application_time,
        working_hours=employer_data.working_hours,
        salary=employer_data.salary,
        additional=employer_data.additional,
        is_sent=False,
        created_at=datetime.now(tz),
        updated_at=datetime.now(tz)
    )
    db.add(employer)
    db.commit()
    db.refresh(employer)
    return employer


@employer_router.message(F.text == "Ish beruvchi")
async def process_employer(message: Message, state: FSMContext):
    await state.update_data(user_type="Employer")
    await state.set_state(EmployerForm.office)
    await message.answer(
        "Iltimos, ofis nomini kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )


@employer_router.message(EmployerForm.office)
async def process_office(message: Message, state: FSMContext):
    await state.update_data(office=message.text)
    await state.set_state(EmployerForm.technology)
    await message.answer("Texnologiyani kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employer_router.message(EmployerForm.technology)
async def process_technology(message: Message, state: FSMContext):
    tech = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(technology=tech)
    await state.set_state(EmployerForm.telegram_username)
    await message.answer("Telegram foydalanuvchi nomini kiriting (@ bilan):")


@employer_router.message(EmployerForm.telegram_username)
async def process_telegram_username(message: Message, state: FSMContext):
    try:
        validated_username = validate_telegram_username(message.text)
        await state.update_data(telegram_username=validated_username)
        await state.set_state(EmployerForm.area)
        await message.answer("Hududni kiriting (yoki 'o'tkazib yuborish' deb yozing):")
    except ValidationError as e:
        await message.answer(f"Noto'g'ri Telegram nomi: {str(e)}")


@employer_router.message(EmployerForm.area)
async def process_area(message: Message, state: FSMContext):
    area = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(area=area)
    await state.set_state(EmployerForm.responsible)
    await message.answer("Mas'ul shaxs nomini kiriting:")


@employer_router.message(EmployerForm.responsible)
async def process_responsible(message: Message, state: FSMContext):
    await state.update_data(responsible=message.text)
    await state.set_state(EmployerForm.application_time)
    await message.answer("Ariza vaqtini kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employer_router.message(EmployerForm.application_time)
async def process_application_time(message: Message, state: FSMContext):
    app_time = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(application_time=app_time)
    await state.set_state(EmployerForm.working_hours)
    await message.answer("Ish vaqtini kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employer_router.message(EmployerForm.working_hours)
async def process_working_hours(message: Message, state: FSMContext):
    hours = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(working_hours=hours)
    await state.set_state(EmployerForm.salary)
    await message.answer("Maoshni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employer_router.message(EmployerForm.salary)
async def process_salary(message: Message, state: FSMContext):
    salary = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(salary=salary)
    await state.set_state(EmployerForm.additional)
    await message.answer("Qo'shimcha ma'lumotlarni kiriting (yoki 'o'tkazib yuborish' deb yozing):")


@employer_router.message(EmployerForm.additional)
async def process_additional(message: Message, state: FSMContext):
    additional = None if message.text.lower() == "o'tkazib yuborish" else message.text
    await state.update_data(additional=additional)

    db = None
    try:
        data = await state.get_data()
        employer_data = EmployerModel(**data)

        db = next(get_db())
        await save_employer_to_db(db, employer_data)

        await state.clear()
        await message.answer("✅ Ish beruvchi sifatida ro'yxatdan o'tish muvaffaqiyatli yakunlandi!")
    except ValidationError as e:
        await message.answer(f"❌ Ma'lumotlarda xatolik: {str(e)}")
    except Exception as e:
        logger.error(f"Error saving employer: {str(e)}", exc_info=True)
        await message.answer("❌ Texnik xatolik yuz berdi. Iltimos, keyinroq urunib ko'ring.")
    finally:
        if db is not None:
            db.close()