from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Register_User(BaseModel):

    nickname: str = Field(max_length=30)

    email: EmailStr

    password: str

class Login_User(BaseModel):

    nickname: str

    email: EmailStr

    password: str


class Refresh_Token(BaseModel):

    refresh_token: str
