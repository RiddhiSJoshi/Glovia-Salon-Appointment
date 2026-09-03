
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StaffCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=10, max_length=20)
    specialization: str | None = Field(None, max_length=150)


class StaffUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    email: EmailStr | None = None
    phone: str | None = Field(None, min_length=10, max_length=20)
    specialization: str | None = Field(None, max_length=150)
    is_active: bool | None = None


class StaffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    salon_id: int
    name: str
    email: str | None
    phone: str | None
    specialization: str | None
    is_active: bool