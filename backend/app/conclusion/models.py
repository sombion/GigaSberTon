from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Conclusion(Base):
    __tablename__ = "conclusion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    applications_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    file_url: Mapped[str] = mapped_column(nullable=True)
