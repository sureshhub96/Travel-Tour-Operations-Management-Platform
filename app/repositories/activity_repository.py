from sqlalchemy.orm import Session

from app.models.activity import Activity


class ActivityRepository:

    @staticmethod
    def create(
        db: Session,
        activity: Activity
    ):
        db.add(activity)
        db.commit()
        db.refresh(activity)

        return activity

    @staticmethod
    def get_by_id(
        db: Session,
        activity_id: int
    ):
        return db.query(Activity).filter(
            Activity.id == activity_id
        ).first()

    @staticmethod
    def get_all(
        db: Session,
        package_id: int | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Activity)

        if package_id is not None:
            query = query.filter(
                Activity.package_id == package_id
            )

        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_package(
        db: Session,
        package_id: int
    ):
        return db.query(Activity).filter(
            Activity.package_id == package_id
        ).all()

    @staticmethod
    def update(
        db: Session,
        activity: Activity
    ):
        db.commit()
        db.refresh(activity)

        return activity

    @staticmethod
    def delete(
        db: Session,
        activity: Activity
    ):
        db.delete(activity)
        db.commit()