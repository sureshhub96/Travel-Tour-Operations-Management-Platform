from datetime import time

from pydantic import BaseModel, Field, model_validator


class ItineraryBase(BaseModel):

    day_number: int = Field(
        ...,
        gt=0
    )

    title: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    description: str | None = None

    location: str | None = None

    start_time: time

    end_time: time

    @model_validator(mode="after")
    def validate_time(self):

        if self.end_time <= self.start_time:
            raise ValueError(
                "End time must be after start time"
            )

        return self


class ItineraryCreate(ItineraryBase):
    pass


class ItineraryUpdate(BaseModel):

    day_number: int | None = Field(
        None,
        gt=0
    )

    title: str | None = None

    description: str | None = None

    location: str | None = None

    start_time: time | None = None

    end_time: time | None = None


class ItineraryResponse(ItineraryBase):

    id: int
    package_id: int

    class Config:
        from_attributes = True