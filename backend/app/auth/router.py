from typing import Any
from fastapi import APIRouter, Depends, Request, Response, status
from app.auth.dependency import get_current_user
from app.auth.models import Users
from app.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    SEditEmail,
    SEditFIO,
    SEditPassword,
)
from app.auth.service import (
    register,
    login,
    logout,
    update_fio,
    update_email,
    update_password,
)

router = APIRouter(prefix="/api/auth", tags=["API Регистрации"])


@router.get("/me")
async def me_api(current_user=Depends(get_current_user)):
    return current_user


@router.post("/register")
async def register_api(payload: RegisterRequest, response: Response):
    return await register(
        response, payload.login, payload.fio, payload.email, payload.password
    )


@router.post("/login")
async def login_api(payload: LoginRequest, response: Response):
    return await login(response, payload.login, payload.password)


@router.post("/logout")
async def logout_api(request: Request, response: Response):
    return await logout(request, response)


@router.post("/edit-fio")
async def update_fio_api(
    user_data: SEditFIO, current_user: Users = Depends(get_current_user)
):
    return await update_fio(current_user.id, user_data.fio)


@router.post("/edit-email")
async def update_email_api(
    user_date: SEditEmail, current_user: Users = Depends(get_current_user)
):
    return await update_email(current_user.id, user_date.email)


@router.post("/edit-password")
async def update_password_api(
    user_date: SEditPassword, current_user: Users = Depends(get_current_user)
):
    return await update_password(
        current_user.id,
        user_date.last_password,
        user_date.new_password,
        user_date.confirm_password,
    )
