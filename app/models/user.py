from sqlalchemy import String, Boolean, Integer
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    
    blood_group_id: Mapped[int] = mapped_column(Integer)
    division_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    upazila_id: Mapped[int] = mapped_column(Integer)

    last_donation_date: Mapped[Optional[date]] = mapped_column(default=None)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)