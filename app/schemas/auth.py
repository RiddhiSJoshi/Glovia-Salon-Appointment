from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class SignupRequest(BaseModel):

    username: EmailStr

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
    def validate_passwords(self):

        if self.password != self.confirmpassword:
            raise ValueError(
                "Password and confirm password do not match"
            )

        return self


class LoginRequest(BaseModel):

    username: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128,
    )


class UserResponse(BaseModel):

    id: int
    username: EmailStr
    firstname: str
    lastname: str
    role: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):

    access_token: str
    refresh_token: str

    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):

    username: EmailStr


class ResetPasswordRequest(BaseModel):

    token: str

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    confirmpassword: str = Field(
        min_length=8,
        max_length=128,
    )

    @model_validator(mode="after")
    def validate_passwords(self):

        if self.password != self.confirmpassword:
            raise ValueError(
                "Password and confirm password do not match"
            )

        return self