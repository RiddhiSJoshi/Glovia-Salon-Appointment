from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class RegisterRequest(BaseModel):

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


class LoginRequest(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        min_length=1,
        max_length=128,
    )


class RefreshTokenRequest(BaseModel):

    refresh_token: str = Field(
        min_length=1,
    )


class TokenResponse(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LogoutRequest(BaseModel):

    refresh_token: str = Field(
        min_length=1,
    )


class UserResponse(BaseModel):

    id: int
    username: str
    firstname: str
    lastname: str
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )