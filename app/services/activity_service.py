from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.package import TourPackage


class ActivityService:

    @staticmethod
    def create(
        db: Session,
        data
    ):

        package = db.query(TourPackage).filter(
            TourPackage.id == data.package_id
        ).first()

        if not package:
            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        if package.status == "Cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cannot add activity to cancelled package"
            )

        activity = Activity(
            **data.model_dump()
        )

        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    @staticmethod
    def get_all(
        db: Session
    ):

        return db.query(Activity).all()