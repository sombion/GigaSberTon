import uuid
import datetime
from typing import Optional
from app.auth.dao import UsersDAO
from app.auth.models import Users
from app.session.dao import SessionDAO
from app.session.models import Session


async def create_session(user_id: int, hours_valid: int = 24) -> str:
    token = uuid.uuid4().hex
    now = datetime.datetime.now()
    expires = now + datetime.timedelta(hours=hours_valid)
    sess = await SessionDAO.add(
        token=token, user_id=user_id, created_at=now, expires_at=expires
    )
    return token


async def get_user_by_session_token(token: str) -> Optional[Users]:
    if not token:
        return None
    sess: Session = await SessionDAO.first_session(token)
    if not sess:
        return None
    if sess.expires_at and sess.expires_at < datetime.datetime.now():
        # expired
        await SessionDAO.delete(sess.id)
        return None

    return await UsersDAO.find_by_id(sess.user_id)
