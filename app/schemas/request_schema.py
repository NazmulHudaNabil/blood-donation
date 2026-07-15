from datetime import date
from datetime import datetime

from pydantic import BaseModel


class RequestCreate(BaseModel):
    requester_name: str
    requester_phone: str
    patient_name: str
    hospital: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    units_needed: int
    needed_by: date


class RequestResponse(BaseModel):
    id: int
    requester_name: str
    requester_phone: str
    patient_name: str
    hospital: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    units_needed: int
    needed_by: date
    status: str
    created_at: datetime

    class Config:
        from_attributes = True