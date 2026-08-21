from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db

from app.models.package import TourPackage
from app.models.review import Review
from app.models.user import User

from app.schemas.package import (
    PackageCreate,
    PackageResponse,
    PackageUpdate,
)

from app.schemas.review import ReviewResponse

from app.services.package_service import PackageService
from app.services.guide_service import GuideService
from app.services.review_service import ReviewService


router = APIRouter(
    prefix="/packages",
    tags=["Tour Packages"]
)


# ==================================================
# CREATE PACKAGE
# ==================================================

@router.post(
    "",
    response_model=PackageResponse,
    status_code=201
)
def create_package(
    package: PackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PackageService.create(
        db,
        package
    )


# ==================================================
# GET PACKAGES
# Search + Filtering + Sorting + Pagination
# ==================================================

@router.get(
    "",
    response_model=list[PackageResponse]
)
def get_packages(
    search: str | None = None,
    destination_id: int | None = None,

    min_price: float | None = Query(
        None,
        ge=0
    ),

    max_price: float | None = Query(
        None,
        ge=0
    ),

    min_duration: int | None = Query(
        None,
        ge=1
    ),

    max_duration: int | None = Query(
        None,
        ge=1
    ),

    travel_date: date | None = None,
    status: str | None = None,
    available_only: bool = False,

    min_rating: float | None = Query(
        None,
        ge=0,
        le=5
    ),

    page: int = Query(
        1,
        ge=1
    ),

    limit: int = Query(
        10,
        ge=1,
        le=100
    ),

    sort_by: str = "id",
    sort_order: str = "asc",

    db: Session = Depends(get_db),
):

    query = db.query(TourPackage)

    # ==================================================
    # SEARCH
    # ==================================================

    if search:
        query = query.filter(
            TourPackage.package_name.ilike(
                f"%{search}%"
            )
        )

    # ==================================================
    # DESTINATION
    # ==================================================

    if destination_id is not None:
        query = query.filter(
            TourPackage.destination_id == destination_id
        )

    # ==================================================
    # PRICE RANGE
    # ==================================================

    if min_price is not None:
        query = query.filter(
            TourPackage.base_price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            TourPackage.base_price <= max_price
        )

    # ==================================================
    # DURATION
    # ==================================================

    if min_duration is not None:
        query = query.filter(
            TourPackage.duration_days >= min_duration
        )

    if max_duration is not None:
        query = query.filter(
            TourPackage.duration_days <= max_duration
        )

    # ==================================================
    # TRAVEL DATE
    # ==================================================

    if travel_date is not None:
        query = query.filter(
            TourPackage.start_date <= travel_date,
            TourPackage.end_date >= travel_date
        )

    # ==================================================
    # STATUS
    # ==================================================

    if status:
        query = query.filter(
            TourPackage.status == status
        )

    # ==================================================
    # AVAILABILITY
    # ==================================================

    if available_only:
        query = query.filter(
            TourPackage.available_slots > 0
        )

    # ==================================================
    # RATING
    # ==================================================

    if min_rating is not None:
        query = (
            query
            .outerjoin(
                Review,
                Review.package_id == TourPackage.id
            )
            .group_by(TourPackage.id)
            .having(
                func.coalesce(
                    func.avg(Review.rating),
                    0
                ) >= min_rating
            )
        )

    # ==================================================
    # SORTING
    # ==================================================

    allowed_sort_fields = {
        "id": TourPackage.id,
        "package_name": TourPackage.package_name,
        "base_price": TourPackage.base_price,
        "duration_days": TourPackage.duration_days,
        "start_date": TourPackage.start_date,
        "end_date": TourPackage.end_date,
        "available_slots": TourPackage.available_slots,
    }

    sort_column = allowed_sort_fields.get(
        sort_by,
        TourPackage.id
    )

    if sort_order.lower() == "desc":
        query = query.order_by(
            desc(sort_column)
        )
    else:
        query = query.order_by(
            asc(sort_column)
        )

    # ==================================================
    # PAGINATION
    # ==================================================

    return (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


# ==================================================
# PACKAGE REVIEWS
# ==================================================

@router.get(
    "/{package_id}/reviews",
    response_model=list[ReviewResponse]
)
def get_package_reviews(
    package_id: int,
    db: Session = Depends(get_db),
):
    return ReviewService.get_package_reviews(
        db,
        package_id
    )


# ==================================================
# ASSIGN GUIDE
# ==================================================

@router.post(
    "/{package_id}/assign-guide/{guide_id}"
)
def assign_guide(
    package_id: int,
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    package = GuideService.assign_guide(
        db,
        package_id,
        guide_id
    )

    if not package:
        return {
            "message": "Package or Guide not found"
        }

    return {
        "message": "Guide assigned successfully",
        "package_id": package.id,
        "guide_id": package.guide_id
    }


# ==================================================
# GET SINGLE PACKAGE
# ==================================================

@router.get(
    "/{package_id}",
    response_model=PackageResponse
)
def get_package(
    package_id: int,
    db: Session = Depends(get_db)
):
    return PackageService.get(
        db,
        package_id
    )


# ==================================================
# UPDATE PACKAGE
# ==================================================

@router.put(
    "/{package_id}",
    response_model=PackageResponse
)
def update_package(
    package_id: int,
    package: PackageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PackageService.update(
        db,
        package_id,
        package
    )


# ==================================================
# DELETE PACKAGE
# ==================================================

@router.delete(
    "/{package_id}"
)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    PackageService.delete(
        db,
        package_id
    )

    return {
        "message": "Package deleted successfully"
    }