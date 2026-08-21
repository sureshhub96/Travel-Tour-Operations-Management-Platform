from pydantic import BaseModel, Field
from typing import Optional


class DestinationBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    country: str
    state: Optional[str] = None
    description: Optional[str] = None
    best_season: Optional[str] = None
    status: str = "Active"


class DestinationCreate(DestinationBase):
    pass


class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None
    best_season: Optional[str] = None
    status: Optional[str] = None


class DestinationResponse(DestinationBase):
    id: int

    class Config:
        from_attributes = True