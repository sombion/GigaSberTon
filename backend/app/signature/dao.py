from datetime import datetime
from sqlalchemy import insert, select
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.signature.models import Signature


class SignatureDAO(BaseDAO):
    model = Signature

    @classmethod
    async def add(cls, user_id: int, conclusion_id: int) -> Signature:
        async with async_session_maker() as session:
            stmt = (
                insert(cls.model)
                .values(user_id=user_id, conclusion_id=conclusion_id)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def search(cls, search_text: str | int):
        async with async_session_maker() as session:
            if type(search_text) is int:
                query = select(cls.model).where(
                    cls.model.cadastral_number.ilike(f"%{search_text}%")
                )
            else:
                query = select(cls.model).where(cls.model.fio.ilike(f"%{search_text}%"))
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def filter(cls, region: str | None, departure_date: datetime):
        async with async_session_maker() as session:
            query = select(cls.model)
            if region:
                query = query.where(cls.model.region == region)
            if departure_date:
                query = query.where(cls.model.departure_date == departure_date)

            result = await session.execute(query)
            return result.mappings().all()
