from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):

    package_id: int

    activity_name: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    location: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    duration: int = Field(
        ...,
        gt=0
    )

    price: float = Field(
        ...,
        ge=0
    )

    capacity: int = Field(
        ...,
        gt=0
    )


class ActivityResponse(BaseModel):

    id: int
    package_id: int
    activity_name: str
    location: str
    duration: int
    price: float
    capacity: int

    class Config:
        from_attributes = True