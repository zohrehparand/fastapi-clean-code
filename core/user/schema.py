from pydantic import BaseModel, Field, field_validator


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=250)
    password: str = Field(..., min_length=6)
    password_confirm: str = Field(..., min_length=6)

    @field_validator("password_confirm")
    @classmethod
    def check_passwords_match(cls, password_confirm, validation):
        if password_confirm != validation.data.get("password"):
            raise ValueError("Passwords do not match")
        return password_confirm


class UserRefreshTokenSchema(BaseModel):
    token: str = Field(..., min_length=1)
