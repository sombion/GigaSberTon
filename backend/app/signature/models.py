from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Signature(Base):
    __tablename__ = "signature"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    conclusion_id: Mapped[int] = mapped_column(ForeignKey("conclusion.id"))
