import enum
from datetime import datetime

from sqlalchemy import DateTime
from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column


class ApplicationStatus(enum.Enum):
    ACCEPTED = "Заявление принято"
    VISIT_ASSIGNED = "Назначен выезд"
    COMMISSION_REVIEW = "Заключение на рассмотрении"
    COMMISSION_RESULT = "Результат комиссии"


class Applications(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    # Кто подал заявление
    tg_id: Mapped[int]

    # Данные заявителя
    fio: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]

    # Данные объекта
    cadastral_number: Mapped[str] = mapped_column(index=True)
    address: Mapped[str]
    street: Mapped[str]
    gps_lat: Mapped[float]
    gps_lng: Mapped[float]

    # Путь шаблона
    file_url: Mapped[str] = mapped_column(nullable=True)

    # Статус
    status: Mapped[ApplicationStatus] = mapped_column(
        default=ApplicationStatus.ACCEPTED
    )
    departure_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
