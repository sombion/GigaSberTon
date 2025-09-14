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

class SEditFIO(BaseModel):
    fio: str = Field(...)

class SEditEmail(BaseModel):
    email: EmailStr = Field(...)

class SEditPassword(BaseModel):
    last_password: str = Field(...)
    new_password: str = Field(...)
    confirm_password: str = Field(...)
