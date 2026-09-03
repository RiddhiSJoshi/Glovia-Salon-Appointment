from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator



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