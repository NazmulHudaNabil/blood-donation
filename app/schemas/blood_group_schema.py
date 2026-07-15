from pydantic import BaseModel

class BloodGroupResponse(BaseModel):
    id: str
    name: str
