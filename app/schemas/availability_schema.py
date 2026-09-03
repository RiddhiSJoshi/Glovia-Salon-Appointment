from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class StaffLeaveCreate(BaseModel):
    leave_date: datetime
    reason: str | None = Field(None, max_length=300)


class StaffLeaveResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    staff_id: int
    leave_date: datetime
    reason: str | None