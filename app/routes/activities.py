from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.activity import (
    ActivityCreate,
    ActivityResponse
)

from app.services.activity_service import (
    ActivityService
)


router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


@router.post(
    "",
    response_model=ActivityResponse,
    status_code=201
)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ActivityService.create(
        db,
        activity
    )


@router.get(
    "",
    response_model=list[ActivityResponse]
)
def get_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return ActivityService.get_all(db)