from app.database import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, server_default=func.now())
    read: Mapped[bool] = mapped_column(default=False)
