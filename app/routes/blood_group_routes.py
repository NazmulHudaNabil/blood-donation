from fastapi import APIRouter

from app.schemas.blood_group_schema import BloodGroupResponse
from app.services.blood_group_service import get_all_blood_groups

router = APIRouter(
    prefix="/blood-groups",
    tags=["Blood Groups"],
)

@router.get(
    "",
    response_model=list[BloodGroupResponse],
)
def list_blood_groups():
    return get_all_blood_groups()
