from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLogin,
    ChangePassword,
)

from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
)
from app.utils.security import (
    hash_password,
    verify_password,
)


class AuthService:

    # ==================================================
    # REGISTER
    # ==================================================

    @staticmethod
    def register(
        db: Session,
        data: UserCreate
    ):

        # ----------------------------------------------
        # Check existing email
        # ----------------------------------------------

        existing_user = db.query(User).filter(
            User.email == data.email
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        # ----------------------------------------------
        # Create user
        # ----------------------------------------------

        user = User(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    # ==================================================
    # LOGIN
    # ==================================================

    @staticmethod
    def login(
        db: Session,
        data: UserLogin
    ):

        # ----------------------------------------------
        # Find user
        # ----------------------------------------------

        user = db.query(User).filter(
            User.email == data.email
        ).first()

        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # ----------------------------------------------
        # Check password
        # ----------------------------------------------

        if not verify_password(
            data.password,
            user.password
        ):

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # ----------------------------------------------
        # Check active account
        # ----------------------------------------------

        if not user.is_active:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # ----------------------------------------------
        # Create tokens
        # ----------------------------------------------

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # ==================================================
    # CHANGE PASSWORD
    # ==================================================

    @staticmethod
    def change_password(
        db: Session,
        user: User,
        data: ChangePassword
    ):

        # ----------------------------------------------
        # Verify old password
        # ----------------------------------------------

        if not verify_password(
            data.old_password,
            user.password
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is incorrect"
            )

        # ----------------------------------------------
        # Validate new password
        # ----------------------------------------------

        if len(data.new_password) < 8:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "New password must be at least "
                    "8 characters"
                )
            )

        # ----------------------------------------------
        # Prevent same password
        # ----------------------------------------------

        if verify_password(
            data.new_password,
            user.password
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "New password must be different "
                    "from old password"
                )
            )

        # ----------------------------------------------
        # Update password
        # ----------------------------------------------

        user.password = hash_password(
            data.new_password
        )

        db.commit()
        db.refresh(user)

        return {
            "message": "Password changed successfully"
        }