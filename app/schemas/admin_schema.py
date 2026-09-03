from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AdminUserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminUserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    is_active: bool | None = None
    role: str | None = None


class AdminStatsResponse(BaseModel):
    total_users: int
    total_customers: int
    total_salon_owners: int
    total_admins: int
    total_salons: int
    total_staff: int
    total_services: int
    total_appointments: int
    total_reviews: int

class MessageResponse(BaseModel):
    message: str



class SalonOwnerCreate(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=100,
    )

    firstname: str = Field(
        min_length=2,
        max_length=50,
    )

    lastname: str = Field(
        min_length=2,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    confirmpassword: str = Field(
        min_length=8,
        max_length=128,
    )

    @model_validator(mode="after")
    def validate_password(self):

        if self.password != self.confirmpassword:
            raise ValueError(
                "Password and confirm password do not match"
            )

        return self