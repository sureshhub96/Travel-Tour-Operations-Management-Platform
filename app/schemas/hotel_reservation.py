from datetime import date

from pydantic import BaseModel, Field, ConfigDict, model_validator


class HotelReservationCreate(BaseModel):

    booking_id: int

    room_id: int

    check_in: date

    check_out: date

    number_of_rooms: int = Field(
        ...,
        gt=0
    )

    @model_validator(mode="after")
    def validate_dates(self):

        if self.check_out <= self.check_in:
            raise ValueError(
                "Check-out must be after check-in"
            )

        return self


class HotelReservationResponse(BaseModel):

    id: int
    booking_id: int
    room_id: int
    check_in: date
    check_out: date
    number_of_rooms: int
    total_amount: float
    status: str

    model_config = ConfigDict(
        from_attributes=True
    )