from typing import Any
from fastapi import APIRouter, Depends, Request, Response, status
from backend.auth.dependency import get_current_user
from backend.auth.schemas import RegisterRequest, LoginRequest, UserOut
from backend.auth.service import register, login, logout

router = APIRouter(
    prefix="/auth",
    tags=["API Регистрации"]
)

@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return current_user

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_api(payload: RegisterRequest, response: Response) -> Any:
    return await register(response, payload.login, payload.email, payload.password)

@router.post("/login")
async def login_api(payload: LoginRequest, response: Response):
    return await login(response, payload.login, payload.password)

@router.post("/logout")
async def logout_api(request: Request, response: Response):
    return await logout(request, response)