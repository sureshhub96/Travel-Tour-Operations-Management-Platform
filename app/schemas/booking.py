from datetime import date

from pydantic import BaseModel, Field, model_validator


class BookingCreate(BaseModel):

    customer_id: int

    package_id: int

    booking_date: date

    number_of_travelers: int = Field(
        ...,
        gt=0
    )

    discount: float = Field(
        default=0,
        ge=0
    )

    tax: float = Field(
        default=0,
        ge=0
    )

    @model_validator(mode="after")
    def validate_amounts(self):

        if self.discount < 0:
            raise ValueError(
                "Discount cannot be negative"
            )

        if self.tax < 0:
            raise ValueError(
                "Tax cannot be negative"
            )

        return self


class BookingResponse(BaseModel):

    id: int
    customer_id: int
    package_id: int
    booking_date: date
    number_of_travelers: int
    base_amount: float
    discount: float
    tax: float
    total_amount: float
    booking_status: str

    class Config:
        from_attributes = True