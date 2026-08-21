from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.destination import Destination
from app.models.package import TourPackage
from app.repositories.package_repository import PackageRepository


ALLOWED_STATUSES = {
    "Draft",
    "Published",
    "Full",
    "Completed",
    "Cancelled",
}


class PackageService:

    # =====================================================
    # CREATE PACKAGE
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        data
    ):
        # Check destination
        destination = (
            db.query(Destination)
            .filter(
                Destination.id == data.destination_id
            )
            .first()
        )

        if not destination:
            raise HTTPException(
                status_code=404,
                detail="Destination not found"
            )

        # Check status
        if data.status not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=400,
                detail="Invalid package status"
            )

        # Check capacity
        if data.available_slots > data.max_capacity:
            raise HTTPException(
                status_code=400,
                detail="Available slots cannot exceed maximum capacity"
            )

        # Check dates
        if data.end_date <= data.start_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )

        # Create package
        package = TourPackage(
            package_name=data.package_name,
            destination_id=data.destination_id,
            description=data.description,
            duration_days=data.duration_days,
            base_price=data.base_price,
            max_capacity=data.max_capacity,
            available_slots=data.available_slots,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status
        )

        try:
            db.add(package)
            db.commit()
            db.refresh(package)

        except Exception as e:
            db.rollback()

            print(
                "PACKAGE CREATE ERROR:",
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail=f"Unable to create package: {str(e)}"
            )

        return package

    # =====================================================
    # GET PACKAGE BY ID
    # =====================================================

    @staticmethod
    def get(
        db: Session,
        package_id: int
    ):

        package = (
            db.query(TourPackage)
            .filter(
                TourPackage.id == package_id
            )
            .first()
        )

        if not package:
            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        return package

    # =====================================================
    # UPDATE PACKAGE
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        package_id: int,
        data
    ):

        package = PackageService.get(
            db,
            package_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Check destination
        if "destination_id" in update_data:

            destination = (
                db.query(Destination)
                .filter(
                    Destination.id ==
                    update_data["destination_id"]
                )
                .first()
            )

            if not destination:
                raise HTTPException(
                    status_code=404,
                    detail="Destination not found"
                )

        # Check status
        if (
            "status" in update_data
            and update_data["status"]
            not in ALLOWED_STATUSES
        ):
            raise HTTPException(
                status_code=400,
                detail="Invalid package status"
            )

        # Check capacity
        new_max_capacity = update_data.get(
            "max_capacity",
            package.max_capacity
        )

        new_available_slots = update_data.get(
            "available_slots",
            package.available_slots
        )

        if new_available_slots > new_max_capacity:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Available slots cannot exceed "
                    "maximum capacity"
                )
            )

        # Check dates
        new_start_date = update_data.get(
            "start_date",
            package.start_date
        )

        new_end_date = update_data.get(
            "end_date",
            package.end_date
        )

        if new_end_date <= new_start_date:
            raise HTTPException(
                status_code=400,
                detail="End date must be after start date"
            )

        # Apply updates
        for key, value in update_data.items():
            setattr(
                package,
                key,
                value
            )

        try:
            db.commit()
            db.refresh(package)

        except Exception as e:
            db.rollback()

            print(
                "PACKAGE UPDATE ERROR:",
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail=f"Unable to update package: {str(e)}"
            )

        return package

    # =====================================================
    # DELETE PACKAGE
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        package_id: int
    ):

        package = PackageService.get(
            db,
            package_id
        )

        try:
            PackageRepository.delete(
                db,
                package
            )

        except Exception as e:
            db.rollback()

            print(
                "PACKAGE DELETE ERROR:",
                repr(e)
            )

            raise HTTPException(
                status_code=500,
                detail=f"Unable to delete package: {str(e)}"
            )

        return True