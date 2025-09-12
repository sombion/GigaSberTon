from sqlalchemy import delete, insert, select, update
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.auth.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add(cls, login: str, fio: str, email: str, hash_password: str) -> Users:
        async with async_session_maker() as session:
            stmt = (
                insert(cls.model)
                .values(login=login, fio=fio, email=email, hash_password=hash_password)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, id: int, hash_password: str, new_hash_password: str) -> Users:
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(hash_password=new_hash_password)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()
