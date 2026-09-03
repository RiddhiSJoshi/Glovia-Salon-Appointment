from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AppointmentStatusUpdate(BaseModel):
    status: str

class AppointmentCreate(BaseModel):
    salon_id: int = Field(..., gt=0)
    staff_id: int = Field(..., gt=0)
    service_id: int = Field(..., gt=0)
    start_time: datetime

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime):
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)

        return value


class AppointmentReschedule(BaseModel):
    start_time: datetime

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime):
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)

        return value

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