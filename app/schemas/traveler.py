from datetime import date

from pydantic import BaseModel, Field, field_validator


class TravelerCreate(BaseModel):

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    date_of_birth: date

    gender: str = Field(
        ...,
        min_length=1,
        max_length=20
    )

    passport_number: str | None = Field(
        default=None,
        max_length=50
    )

    nationality: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    special_requirements: str | None = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value):

        if value >= date.today():
            raise ValueError(
                "Date of birth must be in the past"
            )

        return value


class TravelerUpdate(BaseModel):

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    date_of_birth: date | None = None

    gender: str | None = None

    passport_number: str | None = None

    nationality: str | None = None

    special_requirements: str | None = None


class TravelerResponse(BaseModel):

    id: int
    booking_id: int
    full_name: str
    date_of_birth: date
    gender: str
    passport_number: str | None
    nationality: str
    special_requirements: str | None

    class Config:
        from_attributes = True