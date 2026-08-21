from pydantic import BaseModel, Field


class HotelCreate(BaseModel):

    hotel_name: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    destination_id: int

    address: str | None = None

    rating: float | None = Field(
        default=None,
        ge=0,
        le=5
    )

    contact_number: str | None = None


class HotelResponse(BaseModel):

    id: int
    hotel_name: str
    destination_id: int
    address: str | None
    rating: float | None
    contact_number: str | None

    class Config:
        from_attributes = True