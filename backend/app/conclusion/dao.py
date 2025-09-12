from datetime import datetime
from sqlalchemy import delete, insert, select, update
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.conclusion.models import Conclusion


class ConclusionDAO(BaseDAO):
    model = Conclusion

    @classmethod
    async def add(cls) -> Conclusion:
        async with async_session_maker() as session:
            stmt = insert(cls.model).values().returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, id: int) -> Conclusion:
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id)
                .values()
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
