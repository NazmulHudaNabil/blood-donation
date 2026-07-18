from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator

from app.utils.reference_data import validate_blood_group_id
from app.utils.reference_data import validate_location_ids


class RequestCreate(BaseModel):
    requester_name: str
    requester_phone: str
    patient_name: str
    hospital: str | None = None
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    area: str | None = None
    units_needed: int = Field(default=1, ge=1, le=20)
    needed_by: date

    @model_validator(mode="after")
    def _validate_reference_ids(self):
        validate_blood_group_id(self.blood_group_id)
        validate_location_ids(
            division_id=self.division_id,
            district_id=self.district_id,
            upazila_id=self.upazila_id,
        )
        if self.needed_by < date.today():
            raise ValueError("needed_by cannot be in the past")
        return self


class RequestResponse(BaseModel):
    id: int
    requester_name: str
    requester_phone: str
    patient_name: str
    hospital: str | None = None
    blood_group_id: int
    division_id: int
    district_id: int
    upazila_id: int
    area: str | None = None
    units_needed: int
    needed_by: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)