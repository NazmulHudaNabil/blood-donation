from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user_schema import UserResponse
from app.schemas.user_schema import UserUpdate

from app.models.user import User

from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.put(
    "/me",
    response_model=UserResponse,
)
def update_my_profile(
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.name = user.name
    current_user.phone = user.phone
    current_user.blood_group_id = user.blood_group_id
    current_user.division_id = user.division_id
    current_user.district_id = user.district_id
    current_user.upazila_id = user.upazila_id
    current_user.area = user.area
    current_user.is_available = user.is_available

    db.commit()
    db.refresh(current_user)

    return current_user