import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def _utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class BloodRequest(Base):
    __tablename__ = "blood_requests"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    requester_name: Mapped[str] = mapped_column(String(100))
    requester_phone: Mapped[str] = mapped_column(String(15))
    patient_name: Mapped[str] = mapped_column(String(100))
    hospital: Mapped[Optional[str]] = mapped_column(String(150), default=None)

    blood_group_id: Mapped[int] = mapped_column(Integer)
    division_id: Mapped[int] = mapped_column(Integer)
    district_id: Mapped[int] = mapped_column(Integer)
    upazila_id: Mapped[int] = mapped_column(Integer)
    area: Mapped[Optional[str]] = mapped_column(String(150), default=None)

    units_needed: Mapped[int] = mapped_column(Integer, default=1)
    needed_by: Mapped[datetime.date]
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=_utcnow)