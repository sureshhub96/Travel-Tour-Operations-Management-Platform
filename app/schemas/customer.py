from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    email: EmailStr

    phone: str | None = None

    address: str | None = None

    emergency_contact: str | None = None


class CustomerUpdate(BaseModel):

    name: str | None = Field(
        None,
        min_length=2,
        max_length=150
    )

    email: EmailStr | None = None

    phone: str | None = None

    address: str | None = None

    emergency_contact: str | None = None


class CustomerResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    phone: str | None
    address: str | None
    emergency_contact: str | None

    class Config:
        from_attributes = True