from datetime import datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# =========================
# SALON
# =========================

class SalonCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(None, max_length=1000)
    address: str = Field(..., min_length=5, max_length=300)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    pincode: str = Field(..., min_length=4, max_length=10)
    phone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr | None = None


class SalonUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = Field(None, max_length=1000)
    address: str | None = Field(None, min_length=5, max_length=300)
    city: str | None = Field(None, min_length=2, max_length=100)
    state: str | None = Field(None, min_length=2, max_length=100)
    pincode: str | None = Field(None, min_length=4, max_length=10)
    phone: str | None = Field(None, min_length=10, max_length=20)
    email: EmailStr | None = None
    is_active: bool | None = None


class SalonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    description: str | None
    address: str
    city: str
    state: str
    pincode: str
    phone: str
    email: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


# =========================
# CATEGORY
# =========================

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=500)


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=500)
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    salon_id: int
    name: str
    description: str | None
    is_active: bool


# =========================
# SERVICE
# =========================

class ServiceCreate(BaseModel):
    category_id: int | None = None
    name: str = Field(..., min_length=2, max_length=150)
    description: str | None = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    duration_minutes: int = Field(..., gt=0, le=600)


class ServiceUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(None, min_length=2, max_length=150)
    description: str | None = Field(None, max_length=1000)
    price: Decimal | None = Field(
        None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )
    duration_minutes: int | None = Field(
        None,
        gt=0,
        le=600,
    )
    is_active: bool | None = None


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    salon_id: int
    category_id: int | None
    name: str
    description: str | None
    price: Decimal
    duration_minutes: int
    is_active: bool


# =========================
# STAFF
# =========================

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


# =========================
# WORKING HOURS
# =========================

class WorkingHourCreate(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    opening_time: time
    closing_time: time
    is_closed: bool = False

    @field_validator("closing_time")
    @classmethod
    def validate_time(cls, value, info):
        opening_time = info.data.get("opening_time")

        if opening_time and not info.data.get("is_closed"):
            if value <= opening_time:
                raise ValueError(
                    "Closing time must be after opening time"
                )

        return value


class WorkingHourResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    salon_id: int
    day_of_week: int
    opening_time: time
    closing_time: time
    is_closed: bool


# =========================
# STAFF LEAVE
# =========================

class StaffLeaveCreate(BaseModel):
    leave_date: datetime
    reason: str | None = Field(None, max_length=300)


class StaffLeaveResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    staff_id: int
    leave_date: datetime
    reason: str | None


# =========================
# APPOINTMENT
# =========================

class AppointmentStatusUpdate(BaseModel):
    status: str


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    salon_id: int
    staff_id: int
    service_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime