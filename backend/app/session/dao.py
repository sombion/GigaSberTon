from datetime import datetime
from sqlalchemy import delete, insert, select, update
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.session.models import Session


class SessionDAO(BaseDAO):
    model = Session

    @classmethod
    async def first_session(cls, token):
        async with async_session_maker() as session:
            query = select(cls.model).filter(cls.model.token == token)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add(
        cls, token: str, user_id: int, created_at: datetime, expires_at: datetime
    ) -> Session:
        async with async_session_maker() as session:
            stmt = (
                insert(cls.model)
                .values(
                    token=token,
                    user_id=user_id,
                    created_at=created_at,
                    expires_at=expires_at,
                )
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def delete_session(cls, token: str) -> Session:
        async with async_session_maker() as session:
            stmt = (
                delete(cls.model).where(cls.model.token == token).returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def delete_all_sessions_for_user(cls, user_id: int) -> Session:
        async with async_session_maker() as session:
            stmt = (
                delete(cls.model)
                .where(cls.model.user_id == user_id)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
