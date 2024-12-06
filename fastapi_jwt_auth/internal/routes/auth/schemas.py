from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union


class RegisterUserSchema(BaseModel):

    nickname: str = Field(max_length=30)

    email: EmailStr

    password: str

class LoginUserSchema(BaseModel):

    nickname_or_email: Optional[Union[str, EmailStr]]

    password: str



class RefreshTokenSchema(BaseModel):

    refresh_token: str


class SecureEndpointSchemas(BaseModel):

    access_token: str