from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User

from app.schemas.itinerary import (
    ItineraryCreate,
    ItineraryResponse,
    ItineraryUpdate,
)

from app.services.itinerary_service import (
    ItineraryService,
)


router = APIRouter(
    tags=["Itinerary"]
)


@router.post(
    "/packages/{package_id}/itinerary",
    response_model=ItineraryResponse,
    status_code=201
)
def create_itinerary(
    package_id: int,
    itinerary: ItineraryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ItineraryService.create(
        db,
        package_id,
        itinerary
    )


@router.get(
    "/packages/{package_id}/itinerary",
    response_model=list[ItineraryResponse]
)
def get_package_itinerary(
    package_id: int,
    db: Session = Depends(get_db)
):

    return ItineraryService.get_by_package(
        db,
        package_id
    )


@router.put(
    "/itinerary/{itinerary_id}",
    response_model=ItineraryResponse
)
def update_itinerary(
    itinerary_id: int,
    itinerary: ItineraryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ItineraryService.update(
        db,
        itinerary_id,
        itinerary
    )


@router.delete(
    "/itinerary/{itinerary_id}"
)
def delete_itinerary(
    itinerary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    ItineraryService.delete(
        db,
        itinerary_id
    )

    return {
        "message": "Itinerary deleted successfully"
    }