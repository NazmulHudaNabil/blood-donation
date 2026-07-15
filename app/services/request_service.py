from sqlalchemy.orm import Session
from app.models.request import BloodRequest

def create_request(
    request,
    db: Session,
):
    new_request = BloodRequest(**request.model_dump())
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

def get_requests(
    db: Session,
    blood_group_id: int | None,
    district_id: int | None,
):
    query = db.query(BloodRequest).filter(
        BloodRequest.status == "pending"
    )

    if blood_group_id:
        query = query.filter(
            BloodRequest.blood_group_id == blood_group_id
        )

    if district_id:
        query = query.filter(
            BloodRequest.district_id == district_id
        )

    return query.all()

def fulfill_request(
    request_id: int,
    db: Session,
):
    request = (
        db.query(BloodRequest)
        .filter(BloodRequest.id == request_id)
        .first()
    )

    if not request:
        return None

    request.status = "fulfilled"
    db.commit()
    db.refresh(request)
    return request