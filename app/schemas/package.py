from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class PackageBase(BaseModel):

    package_name: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    destination_id: int

    description: Optional[str] = None

    duration_days: int = Field(
        ...,
        gt=0
    )

    base_price: float = Field(
        ...,
        gt=0
    )

    max_capacity: int = Field(
        ...,
        gt=0
    )

    available_slots: int = Field(
        ...,
        ge=0
    )

    start_date: date

    end_date: date

    status: str = "Draft"

    @model_validator(mode="after")
    def validate_package(self):

        if self.end_date <= self.start_date:
            raise ValueError(
                "End date must be after start date"
            )

        if self.available_slots > self.max_capacity:
            raise ValueError(
                "Available slots cannot exceed maximum capacity"
            )

        return self


class PackageCreate(PackageBase):
    pass


class PackageUpdate(BaseModel):

    package_name: Optional[str] = None

    destination_id: Optional[int] = None

    description: Optional[str] = None

    duration_days: Optional[int] = Field(
        None,
        gt=0
    )

    base_price: Optional[float] = Field(
        None,
        gt=0
    )

    max_capacity: Optional[int] = Field(
        None,
        gt=0
    )

    available_slots: Optional[int] = Field(
        None,
        ge=0
    )

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    status: Optional[str] = None


class PackageResponse(PackageBase):

    id: int

    class Config:
        from_attributes = True