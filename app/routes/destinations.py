from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.destination import Destination
from app.models.user import User
from app.schemas.destination import (
    DestinationCreate,
    DestinationResponse,
    DestinationUpdate,
)
from app.services.destination_service import DestinationService


router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"]
)


@router.post("", response_model=DestinationResponse)
def create_destination(
    destination: DestinationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DestinationService.create(db, destination)


@router.get("", response_model=list[DestinationResponse])
def get_destinations(
    search: str | None = None,
    country: str | None = None,
    season: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Destination)

    if search:
        query = query.filter(Destination.name.ilike(f"%{search}%"))

    if country:
        query = query.filter(Destination.country == country)

    if season:
        query = query.filter(Destination.best_season == season)

    return (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


@router.get("/{destination_id}", response_model=DestinationResponse)
def get_destination(destination_id: int, db: Session = Depends(get_db)):
    return DestinationService.get(db, destination_id)


@router.put("/{destination_id}", response_model=DestinationResponse)
def update_destination(
    destination_id: int,
    destination: DestinationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DestinationService.update(db, destination_id, destination)


@router.delete("/{destination_id}")
def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    DestinationService.delete(db, destination_id)
    return {"message": "Destination deleted successfully"}