from pydantic import BaseModel, EmailStr, Field, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInput(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3)
    password: str
    confirm_password: str

    @validator('confirm_password')
    def password_match(cls, confirm_password, values, **kwargs):
        if 'password' in values and confirm_password != values["password"]:
            raise ValueError("password not match")
        return confirm_password


class UserOutput(BaseModel):
    email: EmailStr
    username: str
