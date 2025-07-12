from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from app.database.base import Base
import pytz
from datetime import datetime

tz = pytz.timezone("Asia/Tashkent")


class Employer(Base):
    __tablename__ = 'employers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    office = Column(String(150), nullable=False)
    technology = Column(String(100), nullable=True)
    telegram_username = Column(String(50), nullable=False)
    area = Column(String(100), nullable=True)
    responsible = Column(String(100), nullable=False)
    application_time = Column(String(50), nullable=True)
    working_hours = Column(String(50), nullable=True)
    salary = Column(String(50), nullable=True)
    additional = Column(Text, nullable=True)

    is_sent = Column(Boolean, default=False, server_default='false', nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(tz), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(tz),
                        onupdate=lambda: datetime.now(tz), nullable=False)

    def __repr__(self):
        return f"<Employer(id={self.id}, office='{self.office}', responsible='{self.responsible}')>"
