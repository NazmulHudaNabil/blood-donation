from fastapi import APIRouter

from app.schemas.location_schema import DivisionResponse, DistrictResponse, UpazilaResponse
from app.services.location_service import (
    get_divisions,
    get_districts_by_division,
    get_upazilas_by_district,
)

router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
)

@router.get(
    "/divisions",
    response_model=list[DivisionResponse],
)
def list_divisions():
    return get_divisions()


@router.get(
    "/divisions/{division_id}/districts",
    response_model=list[DistrictResponse],
)
def list_districts(
    division_id: int,
):
    return get_districts_by_division(division_id)


@router.get(
    "/districts/{district_id}/upazilas",
    response_model=list[UpazilaResponse],
)
def list_upazilas(
    district_id: int,
):
    return get_upazilas_by_district(district_id)
