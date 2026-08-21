from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str
    ):
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class AuthenticationException(AppException):
    def __init__(
        self,
        detail: str = "Authentication failed"
    ):
        super().__init__(
            status.HTTP_401_UNAUTHORIZED,
            detail
        )


class AuthorizationException(AppException):
    def __init__(
        self,
        detail: str = "You do not have permission"
    ):
        super().__init__(
            status.HTTP_403_FORBIDDEN,
            detail
        )


class NotFoundException(AppException):
    def __init__(
        self,
        detail: str = "Resource not found"
    ):
        super().__init__(
            status.HTTP_404_NOT_FOUND,
            detail
        )


class BadRequestException(AppException):
    def __init__(
        self,
        detail: str = "Invalid request"
    ):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail
        )


class ConflictException(AppException):
    def __init__(
        self,
        detail: str = "Resource already exists"
    ):
        super().__init__(
            status.HTTP_409_CONFLICT,
            detail
        )


class BusinessRuleException(AppException):
    def __init__(
        self,
        detail: str = "Business rule violation"
    ):
        super().__init__(
            status.HTTP_400_BAD_REQUEST,
            detail
        )