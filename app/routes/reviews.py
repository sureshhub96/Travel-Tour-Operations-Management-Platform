from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse
)

from app.services.review_service import ReviewService


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews & Ratings"]
)


# -----------------------------------------
# Create Review
# -----------------------------------------

@router.post(
    "",
    response_model=ReviewResponse,
    status_code=201
)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ReviewService.create(
        db,
        current_user.id,
        data
    )


# -----------------------------------------
# Update Review
# -----------------------------------------

@router.put(
    "/{review_id}",
    response_model=ReviewResponse
)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ReviewService.update(
        db,
        review_id,
        current_user.id,
        data
    )


# -----------------------------------------
# Delete Review
# -----------------------------------------

@router.delete(
    "/{review_id}"
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ReviewService.delete(
        db,
        review_id,
        current_user.id
    )