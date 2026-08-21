from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    # ==================================================
    # CREATE USER
    # ==================================================

    @staticmethod
    def create(
        db: Session,
        user: User
    ):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    # ==================================================
    # GET USER BY ID
    # ==================================================

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ):
        return db.query(User).filter(
            User.id == user_id
        ).first()

    # ==================================================
    # GET USER BY EMAIL
    # ==================================================

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):
        return db.query(User).filter(
            User.email == email
        ).first()

    # ==================================================
    # GET ALL USERS
    # ==================================================

    @staticmethod
    def get_all(
        db: Session,
        role: str | None = None,
        is_active: bool | None = None,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(User)

        # Role filter
        if role:
            query = query.filter(
                User.role == role
            )

        # Active/inactive filter
        if is_active is not None:
            query = query.filter(
                User.is_active == is_active
            )

        # Pagination
        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    # ==================================================
    # UPDATE USER
    # ==================================================

    @staticmethod
    def update(
        db: Session,
        user: User
    ):
        db.commit()
        db.refresh(user)

        return user

    # ==================================================
    # DEACTIVATE USER
    # ==================================================

    @staticmethod
    def deactivate(
        db: Session,
        user: User
    ):
        user.is_active = False

        db.commit()
        db.refresh(user)

        return user

    # ==================================================
    # ACTIVATE USER
    # ==================================================

    @staticmethod
    def activate(
        db: Session,
        user: User
    ):
        user.is_active = True

        db.commit()
        db.refresh(user)

        return user

    # ==================================================
    # DELETE USER
    # ==================================================

    @staticmethod
    def delete(
        db: Session,
        user: User
    ):
        db.delete(user)
        db.commit()

        return True