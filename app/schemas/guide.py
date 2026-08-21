from pydantic import BaseModel
from typing import Optional


class GuideBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: int = 0
    bio: Optional[str] = None
    is_available: bool = True


class GuideCreate(GuideBase):
    pass


class GuideUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    is_available: Optional[bool] = None


class GuideResponse(GuideBase):
    id: int

    class Config:
        from_attributes = True