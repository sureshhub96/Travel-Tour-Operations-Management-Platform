from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.guide import Guide
from app.models.package import TourPackage
from app.schemas.guide import GuideCreate, GuideUpdate


class GuideService:

    # =====================================================
    # CREATE GUIDE
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        guide_data: GuideCreate
    ):
        existing_guide = (
            db.query(Guide)
            .filter(Guide.email == guide_data.email)
            .first()
        )

        if existing_guide:
            raise HTTPException(
                status_code=400,
                detail="Guide email already exists"
            )

        guide = Guide(
            name=guide_data.name,
            email=guide_data.email,
            phone=guide_data.phone,
            language=guide_data.language,
            specialization=guide_data.specialization,
            experience_years=guide_data.experience_years,
            bio=guide_data.bio,
            is_available=guide_data.is_available
        )

        db.add(guide)
        db.commit()
        db.refresh(guide)

        return guide

    # =====================================================
    # GET ALL GUIDES
    # =====================================================

    @staticmethod
    def get_all(
        db: Session
    ):
        return (
            db.query(Guide)
            .order_by(Guide.id)
            .all()
        )

    # =====================================================
    # GET GUIDE BY ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        guide_id: int
    ):
        guide = (
            db.query(Guide)
            .filter(Guide.id == guide_id)
            .first()
        )

        if not guide:
            raise HTTPException(
                status_code=404,
                detail="Guide not found"
            )

        return guide

    # =====================================================
    # UPDATE GUIDE
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        guide_id: int,
        guide_data: GuideUpdate
    ):
        guide = (
            db.query(Guide)
            .filter(Guide.id == guide_id)
            .first()
        )

        if not guide:
            raise HTTPException(
                status_code=404,
                detail="Guide not found"
            )

        update_data = guide_data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:
            existing_guide = (
                db.query(Guide)
                .filter(
                    Guide.email == update_data["email"],
                    Guide.id != guide_id
                )
                .first()
            )

            if existing_guide:
                raise HTTPException(
                    status_code=400,
                    detail="Guide email already exists"
                )

        for key, value in update_data.items():
            setattr(guide, key, value)

        db.commit()
        db.refresh(guide)

        return guide

    # =====================================================
    # DELETE GUIDE
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        guide_id: int
    ):
        guide = (
            db.query(Guide)
            .filter(Guide.id == guide_id)
            .first()
        )

        if not guide:
            raise HTTPException(
                status_code=404,
                detail="Guide not found"
            )

        # Remove guide from package before deleting
        packages = (
            db.query(TourPackage)
            .filter(TourPackage.guide_id == guide_id)
            .all()
        )

        for package in packages:
            package.guide_id = None

        db.delete(guide)
        db.commit()

        return True

    # =====================================================
    # ASSIGN GUIDE TO PACKAGE
    # =====================================================

    @staticmethod
    def assign_guide(
        db: Session,
        package_id: int,
        guide_id: int
    ):
        # -----------------------------
        # Check package
        # -----------------------------

        package = (
            db.query(TourPackage)
            .filter(TourPackage.id == package_id)
            .first()
        )

        if not package:
            raise HTTPException(
                status_code=404,
                detail="Package not found"
            )

        # -----------------------------
        # Check guide
        # -----------------------------

        guide = (
            db.query(Guide)
            .filter(Guide.id == guide_id)
            .first()
        )

        if not guide:
            raise HTTPException(
                status_code=404,
                detail="Guide not found"
            )

        # -----------------------------
        # Check guide availability
        # -----------------------------

        if not guide.is_available:
            raise HTTPException(
                status_code=400,
                detail="Guide is not available"
            )

        # -----------------------------
        # Assign guide
        # -----------------------------

        package.guide_id = guide.id

        # Guide becomes unavailable
        guide.is_available = False

        db.commit()
        db.refresh(package)

        return package