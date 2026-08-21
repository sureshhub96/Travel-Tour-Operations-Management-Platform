from sqlalchemy.orm import Session

from app.models.guide import TourGuide


class GuideRepository:

    @staticmethod
    def create(
        db: Session,
        guide: TourGuide
    ):
        db.add(guide)
        db.commit()
        db.refresh(guide)

        return guide

    @staticmethod
    def get_by_id(
        db: Session,
        guide_id: int
    ):
        return db.query(TourGuide).filter(
            TourGuide.id == guide_id
        ).first()

    @staticmethod
    def get_all(
        db: Session,
        availability_status: str | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(TourGuide)

        if availability_status:
            query = query.filter(
                TourGuide.availability_status ==
                availability_status
            )

        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        guide: TourGuide
    ):
        db.commit()
        db.refresh(guide)

        return guide

    @staticmethod
    def delete(
        db: Session,
        guide: TourGuide
    ):
        db.delete(guide)
        db.commit()