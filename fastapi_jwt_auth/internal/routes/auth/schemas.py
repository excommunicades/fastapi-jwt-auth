from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterUserSchema(BaseModel):

    nickname: str = Field(max_length=30)

    email: EmailStr

    password: str

class LoginUserSchema(BaseModel):

    nickname: str = Field(max_length=30)

    email: EmailStr

    password: str


class RefreshTokenSchema(BaseModel):

    refresh_token: str
