from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException, Request, Response
from backend.auth.models import Users
from backend.auth.dao import UsersDAO
from backend.auth.schemas import UserOut
from backend.session.dao import SessionDAO
from backend.config import settings
from backend.session.service import create_session

pwd_context = CryptContext(schemes=["bcrypt"])

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(login: str, password: str) -> Optional[Users]:
    user: Users = await UsersDAO.find_one_or_none(login=login)
    if not user:
        return None
    if not await verify_password(password, user.hash_password):
        return None
    return user

async def register(response: Response, login: str, email: str, password: str):
    if await UsersDAO.find_one_or_none(login=login):
        raise HTTPException(status_code=400, detail="Login already taken")
    if await UsersDAO.find_one_or_none(email=email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hash_password = await get_password_hash(password)

    user = await UsersDAO.add(login, email, hash_password)

    # создаём сессию сразу
    token = await create_session(user.id)
    # HttpOnly cookie
    response.set_cookie(key=settings.COOKIE_NAME, value=token, httponly=True, samesite="lax")
    return {"message": "ok", "user": user}

async def login(response: Response, login: str, password: str):
    user = await authenticate_user(login, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = await create_session(user.id)
    response.set_cookie(key=settings.COOKIE_NAME, value=token, httponly=True, samesite="lax")
    return {"message": "ok", "user": user}

async def logout(request: Request, response: Response):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        await SessionDAO.delete_session(token)
    response.delete_cookie(settings.COOKIE_NAME)
    return {"message": "logged out"}