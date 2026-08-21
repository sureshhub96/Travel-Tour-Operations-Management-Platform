from sqlalchemy.orm import Session

from app.models.package import TourPackage


class PackageRepository:

    @staticmethod
    def create(
        db: Session,
        package: TourPackage
    ):

        db.add(package)
        db.commit()
        db.refresh(package)

        return package

    @staticmethod
    def get_by_id(
        db: Session,
        package_id: int
    ):

        return db.query(TourPackage).filter(
            TourPackage.id == package_id
        ).first()

    @staticmethod
    def delete(
        db: Session,
        package: TourPackage
    ):

        db.delete(package)
        db.commit()