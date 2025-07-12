from pydantic import BaseModel, validator, Field
from datetime import datetime
from app.utils.validation import (
    validate_telegram_username,
)
import pytz

tz = pytz.timezone("Asia/Tashkent")


def tz_now():
    return datetime.now(tz)


class EmployerModel(BaseModel):
    office: str
    technology: str | None = None
    telegram_username: str
    area: str | None = None
    responsible: str
    application_time: str | None = None
    working_hours: str | None = None
    salary: str | None = None
    additional: str | None = None

    is_sent: bool = False
    created_at: datetime = Field(default_factory=tz_now)
    updated_at: datetime = Field(default_factory=tz_now)

    @validator("telegram_username")
    def validate_telegram(cls, v):
        return validate_telegram_username(v)
