from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database.base import Base

import pytz
from datetime import datetime

tz = pytz.timezone("Asia/Tashkent")

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    technology = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=False)
    telegram_username = Column(String(50), nullable=False)
    area = Column(String(100), nullable=True)
    price = Column(String(50), nullable=True)
    profession = Column(String(100), nullable=True)
    application_time = Column(String(100), nullable=True)
    purpose = Column(String(500), nullable=True)
    is_sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(tz),
                        onupdate=lambda: datetime.now(tz), nullable=False)

    def __repr__(self):
        return f"<Employee(id={self.id}, full_name='{self.full_name}')>"
