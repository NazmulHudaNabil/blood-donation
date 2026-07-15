from pydantic import BaseModel
from typing import Optional


class DivisionResponse(BaseModel):
    id: str
    name: str
    bn_name: str
    lat: str
    long: str

class DistrictResponse(BaseModel):
    id: str
    division_id: str
    name: str
    bn_name: str
    lat: str
    long: str

class UpazilaResponse(BaseModel):
    id: str
    district_id: str
    name: str
    bn_name: str
