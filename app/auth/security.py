from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import settings


# ==================================================
# PASSWORD HASHING
# ==================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# ==================================================
# HASH PASSWORD
# ==================================================

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """

    if not password:
        raise ValueError(
            "Password cannot be empty"
        )

    # bcrypt supports a maximum of 72 bytes
    if len(password.encode("utf-8")) > 72:
        raise ValueError(
            "Password cannot exceed 72 bytes"
        )

    return pwd_context.hash(password)


# ==================================================
# VERIFY PASSWORD
# ==================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain password against
    the stored bcrypt hash.
    """

    if not plain_password or not hashed_password:
        return False

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==================================================
# CREATE JWT TOKEN
# ==================================================

def create_token(
    data: dict,
    expires_delta: timedelta
) -> str:
    """
    Create a JWT token.
    """

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + expires_delta
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# ==================================================
# CREATE ACCESS TOKEN
# ==================================================

def create_access_token(
    user_id: int,
    role: str
) -> str:
    """
    Create JWT access token.
    """

    return create_token(
        {
            "sub": str(user_id),
            "role": role,
            "type": "access",
        },
        timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


# ==================================================
# CREATE REFRESH TOKEN
# ==================================================

def create_refresh_token(
    user_id: int
) -> str:
    """
    Create JWT refresh token.
    """

    return create_token(
        {
            "sub": str(user_id),
            "type": "refresh",
        },
        timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )


# ==================================================
# DECODE TOKEN
# ==================================================

def decode_token(
    token: str
) -> dict:
    """
    Decode and validate a JWT token.
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[
            settings.ALGORITHM
        ]
    )