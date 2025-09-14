from typing import Optional
from passlib.context import CryptContext
from fastapi import HTTPException, Request, Response
from app.auth.models import Users
from app.auth.dao import UsersDAO
from app.session.dao import SessionDAO
from app.config import settings
from app.session.service import create_session

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


async def register(response: Response, login: str, fio: str, email: str, password: str):
    if await UsersDAO.find_one_or_none(login=login):
        raise HTTPException(status_code=400, detail="Login already taken")
    if await UsersDAO.find_one_or_none(email=email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hash_password = await get_password_hash(password)

    user = await UsersDAO.add(login, fio, email, hash_password)

    # создаём сессию сразу
    token = await create_session(user.id)
    # HttpOnly cookie
    response.set_cookie(
        key=settings.COOKIE_NAME, value=token, httponly=True, samesite="lax"
    )
    del user.hash_password
    return {"message": "ok", "user": user}


async def login(response: Response, login: str, password: str):
    user = await authenticate_user(login, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = await create_session(user.id)
    response.set_cookie(
        key=settings.COOKIE_NAME, value=token, httponly=True, samesite="lax"
    )
    del user.hash_password
    return {"message": "ok", "user": user}


async def logout(request: Request, response: Response):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        await SessionDAO.delete_session(token)
    response.delete_cookie(settings.COOKIE_NAME)
    return {"message": "logged out"}

async def update_fio(id: int, fio: str):
    await UsersDAO.update_fio(id, fio)
    return {"detail": "ФИО успешно изменено"}

async def update_email(id: int, email: str):
    await UsersDAO.update_email(id, email)
    return {"detail": "Почта успешно изменена"}

async def update_password(id: int, last_password: str, new_password: str, confirm_password: str):
    if new_password != confirm_password:
        raise {"detail": "Пароли не совпадают"}
    user: Users = await UsersDAO.find_by_id(id)
    if not await verify_password(last_password, user.hash_password):
        raise {"detail": "Текущий пароль не верный"}
    new_hash_password = await get_password_hash(new_password)
    await UsersDAO.update_password(id, new_hash_password)
    return {"detail": "Пароль успешно изменен"}