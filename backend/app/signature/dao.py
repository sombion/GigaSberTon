from datetime import datetime
from sqlalchemy import insert, or_, select, update
from app.applications.models import Applications
from app.conclusion.models import Conclusion
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
    async def update(cls, id: int) -> Signature:
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(signed=False)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def all(cls):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.__table__.columns,
                    Conclusion.__table__.columns,
                    Applications.__table__.columns,
                )
                .join(Conclusion, cls.model.conclusion_id == Conclusion.id)
                .join(Applications, Conclusion.applications_id == Applications.id)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def search(cls, search_text: str | int):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.__table__.columns,
                    Conclusion.__table__.columns,
                    Applications.__table__.columns,
                )
                .join(Conclusion, cls.model.conclusion_id == Conclusion.id)
                .join(Applications, Conclusion.applications_id == Applications.id)
                .where(
                    or_(
                        Applications.cadastral_number.ilike(f"%{search_text}%"),
                        Applications.fio.ilike(f"%{search_text}%")
                    )
                )
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def filter(
        cls,
        street: str | None,
        date_from: datetime | None,
        date_to: datetime | None,
    ):
        async with async_session_maker() as session:
            query = (
                select(
                    cls.model.__table__.columns,
                    Conclusion.__table__.columns,
                    Applications.__table__.columns,
                )
                .join(Conclusion, cls.model.conclusion_id == Conclusion.id)
                .join(Applications, Conclusion.applications_id == Applications.id)
            )
            if street:
                query = query.where(Applications.street == street)

            if date_from and date_to:
                query = query.where(cls.model.create_date.between(date_from, date_to))
            elif date_from:
                query = query.where(cls.model.create_date >= date_from)
            elif date_to:
                query = query.where(cls.model.create_date <= date_to)

            result = await session.execute(query)
            return result.mappings().all()
