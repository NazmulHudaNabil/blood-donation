from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.request_schema import (
    RequestCreate,
    RequestResponse,
)

from app.services.request_service import (
    create_request,
    get_requests,
    fulfill_request,
)

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)

@router.post(
    "",
    response_model=RequestResponse,
)
def create_new_request(
    request: RequestCreate,
    db: Session = Depends(get_db),
):
    return create_request(
        request,
        db,
    )

@router.get(
    "",
    response_model=list[RequestResponse],
)
def list_requests(
    blood_group_id: int | None = None,
    district_id: int | None = None,
    db: Session = Depends(get_db),
):
    return get_requests(
        db,
        blood_group_id,
        district_id,
    )

@router.patch(
    "/{request_id}/fulfill",
    response_model=RequestResponse,
)
def fulfill(
    request_id: int,
    db: Session = Depends(get_db),
):
    request = fulfill_request(
        request_id,
        db,
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found",
        )

    return request