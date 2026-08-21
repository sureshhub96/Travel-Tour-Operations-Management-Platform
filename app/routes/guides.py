from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.schemas.guide import (
    GuideCreate,
    GuideUpdate,
    GuideResponse
)

from app.services.guide_service import GuideService


router = APIRouter(
    prefix="/guides",
    tags=["Guides"]
)


# ==============================
# CREATE GUIDE
# ==============================

@router.post(
    "",
    response_model=GuideResponse,
    status_code=201
)
def create_guide(
    guide: GuideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return GuideService.create(
        db,
        guide
    )


# ==============================
# GET ALL GUIDES
# ==============================

@router.get(
    "",
    response_model=list[GuideResponse]
)
def get_guides(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return GuideService.get_all(db)


# ==============================
# GET SINGLE GUIDE
# ==============================

@router.get(
    "/{guide_id}",
    response_model=GuideResponse
)
def get_guide(
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    guide = GuideService.get_by_id(
        db,
        guide_id
    )

    if not guide:
        raise HTTPException(
            status_code=404,
            detail="Guide not found"
        )

    return guide


# ==============================
# UPDATE GUIDE
# ==============================

@router.put(
    "/{guide_id}",
    response_model=GuideResponse
)
def update_guide(
    guide_id: int,
    guide: GuideUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_guide = GuideService.update(
        db,
        guide_id,
        guide
    )

    if not updated_guide:
        raise HTTPException(
            status_code=404,
            detail="Guide not found"
        )

    return updated_guide


# ==============================
# DELETE GUIDE
# ==============================

@router.delete(
    "/{guide_id}",
    status_code=204
)
def delete_guide(
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = GuideService.delete(
        db,
        guide_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Guide not found"
        )

    return None