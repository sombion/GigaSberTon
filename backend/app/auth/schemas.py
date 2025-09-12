from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    login: str = Field(...)
    fio: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class LoginRequest(BaseModel):
    login: str = Field(...)
    password: str = Field(...)