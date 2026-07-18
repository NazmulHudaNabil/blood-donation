from datetime import date
from pydantic import BaseModel, ConfigDict


class DonorResponse(BaseModel):
    id: int
    name: str
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    area: str | None = None
    phone: str
    is_available: bool
    last_donation_date: date | None

    model_config = ConfigDict(from_attributes=True)


class AvailabilityUpdate(BaseModel):
    is_available: bool