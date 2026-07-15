from datetime import date
from sqlalchemy.orm import Session
from app.models.user import User

def get_all_available_donors(
    db: Session,
    blood_group_id: int,
    district_id: int,
    upazila_id: int | None = None,
):
    query = db.query(User).filter(
        User.is_available == True,
        User.blood_group_id == blood_group_id,
        User.district_id == district_id
    )

    if upazila_id:
        query = query.filter(
            User.upazila_id == upazila_id
        )

    return query.all()


def get_donor_by_id(
    donor_id: int,
    db: Session,
):
    return (
        db.query(User)
        .filter(User.id == donor_id)
        .first()
    )


def update_availability(
    user: User,
    is_available: bool,
    db: Session,
):
    user.is_available = is_available
    db.commit()
    db.refresh(user)
    return user


def mark_as_donated(
    user: User,
    db: Session,
):
    user.last_donation_date = date.today()
    user.is_available = False
    db.commit()
    db.refresh(user)
    return user