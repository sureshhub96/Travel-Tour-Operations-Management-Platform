from datetime import datetime

from pydantic import BaseModel, Field


class CancellationCreate(BaseModel):

    reason: str = Field(
        ...,
        min_length=3,
        max_length=500
    )


class CancellationResponse(BaseModel):

    id: int
    booking_id: int
    cancellation_reason: str
    refund_amount: float
    cancellation_date: datetime

    class Config:
        from_attributes = True