from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    password: str
    last_donation_date: Optional[date] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    last_donation_date: Optional[date]= None
    is_available: bool

    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    name: str
    phone: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    is_available: bool