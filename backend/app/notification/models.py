from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE")
    )
    message: Mapped[str]
    created_at: Mapped[datetime]
    read: Mapped[bool] = mapped_column(default=False)
