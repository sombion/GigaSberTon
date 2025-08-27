from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from sqlalchemy import DateTime, ForeignKey


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    token: Mapped[str] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user = relationship("Users", back_populates="sessions")