from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):

    package_id: int
    booking_id: int

    rating: int = Field(
        ...,
        ge=1,
        le=5
    )

    review_text: str | None = None


class ReviewUpdate(BaseModel):

    rating: int | None = Field(
        None,
        ge=1,
        le=5
    )

    review_text: str | None = None


class ReviewResponse(BaseModel):

    id: int
    customer_id: int
    package_id: int
    booking_id: int
    rating: int
    review_text: str | None
    created_at: datetime

    class Config:
        from_attributes = True