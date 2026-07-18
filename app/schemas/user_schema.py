from datetime import date
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator

from app.utils.reference_data import validate_blood_group_id
from app.utils.reference_data import validate_location_ids


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    area: Optional[str] = None
    password: str = Field(min_length=8, max_length=72)
    last_donation_date: Optional[date] = None

    @field_validator("password")
    @classmethod
    def _password_strength(cls, value: str) -> str:
        if not any(c.isalpha() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one letter and one number")
        return value

    @model_validator(mode="after")
    def _validate_reference_ids(self):
        validate_blood_group_id(self.blood_group_id)
        validate_location_ids(
            division_id=self.division_id,
            district_id=self.district_id,
            upazila_id=self.upazila_id,
        )
        return self


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    area: Optional[str] = None
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
    area: Optional[str] = None
    is_available: bool

    @model_validator(mode="after")
    def _validate_reference_ids(self):
        validate_blood_group_id(self.blood_group_id)
        validate_location_ids(
            division_id=self.division_id,
            district_id=self.district_id,
            upazila_id=self.upazila_id,
        )
        return self