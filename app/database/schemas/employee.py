from pydantic import BaseModel, validator, Field
from datetime import datetime
from app.utils.validation import (
    validate_full_name,
    validate_phone_number,
    validate_telegram_username,
)
import pytz

tz = pytz.timezone("Asia/Tashkent")


def tz_now():
    return datetime.now(tz)


class EmployeeModel(BaseModel):
    full_name: str
    age: int
    technology: str | None = None
    phone_number: str
    telegram_username: str
    area: str | None = None
    price: str | None = None
    profession: str | None = None
    application_time: str | None = None
    purpose: str | None = None

    is_sent: bool = False
    created_at: datetime = Field(default_factory=tz_now)
    updated_at: datetime = Field(default_factory=tz_now)

    @validator("full_name")
    def validate_name(cls, v):
        return validate_full_name(v)

    @validator("phone_number")
    def validate_phone(cls, v):
        return validate_phone_number(v)

    @validator("telegram_username")
    def validate_telegram(cls, v):
        return validate_telegram_username(v)
