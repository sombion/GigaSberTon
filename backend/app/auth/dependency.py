from fastapi import HTTPException, Request
from app.config import settings
from app.session.service import get_user_by_session_token


async def get_current_user(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    user = await get_user_by_session_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    del user.hash_password
    return user
