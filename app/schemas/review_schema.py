from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# CREATE REVIEW
# ============================================================

class ReviewCreate(BaseModel):
    salon_id: int = Field(
        ...,
        gt=0,
        description="ID of the salon being reviewed",
    )

    rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Rating between 1 and 5",
    )

    comment: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional review comment",
    )


# ============================================================
# UPDATE REVIEW
# ============================================================

class ReviewUpdate(BaseModel):
    rating: int | None = Field(
        default=None,
        ge=1,
        le=5,
        description="Rating between 1 and 5",
    )

    comment: str | None = Field(
        default=None,
        max_length=1000,
        description="Optional review comment",
    )


# ============================================================
# RESPONSE
# ============================================================

class ReviewResponse(BaseModel):
    id: int
    customer_id: int
    salon_id: int
    rating: int
    comment: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )