from pydantic import BaseModel, ConfigDict
from typing import Optional


class RoomBase(BaseModel):

    room_number: str

    room_type: str

    capacity: int

    price_per_night: float

    availability_status: str = "Available"


class RoomCreate(RoomBase):

    hotel_id: int


class RoomUpdate(BaseModel):

    room_number: Optional[str] = None

    room_type: Optional[str] = None

    capacity: Optional[int] = None

    price_per_night: Optional[float] = None

    availability_status: Optional[str] = None


class RoomResponse(RoomBase):

    id: int

    hotel_id: int

    model_config = ConfigDict(
        from_attributes=True
    )