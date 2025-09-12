from datetime import datetime
from sqlalchemy import delete, distinct, insert, select, update
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.applications.models import Applications, ApplicationStatus


class ApplicationsDAO(BaseDAO):
    model = Applications

    @classmethod
    async def add(
        cls,
        tg_id: int,
        fio: str,
        phone: str,
        email: str,
        cadastral_number: str,
        region: str,
        gps_lat: int,
        gps_lng: int,
        file_url: str,
    ) -> Applications:
        async with async_session_maker() as session:
            stmt = (
                insert(cls.model)
                .values(
                    tg_id=tg_id,
                    fio=fio,
                    phone=phone,
                    email=email,
                    cadastral_number=cadastral_number,
                    region=region,
                    gps_lat=gps_lat,
                    gps_lng=gps_lng,
                    file_url=file_url,
                )
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            stmt = delete(cls.model).where(cls.model.id == id).returning(cls.model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def update(cls, id: int, status: ApplicationStatus) -> Applications:
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(status=status)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    @classmethod
    async def departure(cls, id: int, departure_date: datetime) -> Applications:
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == id)
                .values(
                    status=ApplicationStatus.VISIT_ASSIGNED,
                    departure_date=departure_date,
                )
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
    async def filter(
        cls, region: str | None, departure_date: datetime, is_departure: bool
    ):
        async with async_session_maker() as session:
            query = select(cls.model)
            if region:
                query = query.where(cls.model.region == region)
            if departure_date:
                query = query.where(cls.model.departure_date == departure_date)
            if is_departure:
                query = query.where(
                    cls.model.status == ApplicationStatus.VISIT_ASSIGNED
                )
            else:
                query = query.where(
                    cls.model.status != ApplicationStatus.VISIT_ASSIGNED
                )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_regions(cls, search: str | None):
        async with async_session_maker() as session:
            query = select(distinct(cls.model.region).label("region"))
            if search:
                query = query.where(cls.model.region.ilike(f"%{search}%"))
            result = await session.execute(query)
            return result.mappings().all()
