from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.schemas.user_schema import UserCreate
from app.schemas.user_schema import UserResponse

from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import LoginRequest
from app.schemas.auth_schema import Token

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        blood_group_id=user.blood_group_id,
        division_id=user.division_id,
        district_id=user.district_id,
        upazila_id=user.upazila_id,
        password=hash_password(user.password),
        last_donation_date=user.last_donation_date,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post(
    "/login",
    response_model=Token,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not verify_password(
        form_data.password,
        db_user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {
            "sub": db_user.email,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }