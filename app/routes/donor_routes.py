from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

from app.schemas.donor_schema import (
    DonorResponse,
    AvailabilityUpdate,
)

from app.services.donor_service import (
    get_all_available_donors,
    get_donor_by_id,
    update_availability,
    mark_as_donated,
)

from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/donors",
    tags=["Donors"],
)

@router.get(
    "",
    response_model=list[DonorResponse],
)
def list_donors(
    blood_group_id: int,
    district_id: int,
    upazila_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_all_available_donors(
        db=db,
        blood_group_id=blood_group_id,
        district_id=district_id,
        upazila_id=upazila_id,
    )


@router.get(
    "/{donor_id}",
    response_model=DonorResponse,
)
def donor_profile(
    donor_id: int,
    db: Session = Depends(get_db),
):
    donor = get_donor_by_id(
        donor_id,
        db,
    )

    if donor is None:
        raise HTTPException(
            status_code=404,
            detail="Donor not found",
        )

    return donor


@router.patch(
    "/me/availability",
    response_model=DonorResponse,
)
def change_availability(
    data: AvailabilityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_availability(
        current_user,
        data.is_available,
        db,
    )


@router.patch(
    "/me/donated",
    response_model=DonorResponse,
)
def donated(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return mark_as_donated(
        current_user,
        db,
    )