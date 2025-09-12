from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    login: Mapped[str] = mapped_column(unique=True, index=True)
    fio: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hash_password: Mapped[str]
