from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    login: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hash_password: Mapped[str]

    sessions = relationship("Session", back_populates="user")