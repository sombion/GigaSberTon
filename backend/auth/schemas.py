from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    login: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    login: str
    password: str


class UserOut(BaseModel):
    id: int
    login: str
    email: str


    class Config:
        orm_mode = True