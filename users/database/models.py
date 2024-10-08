from datetime import datetime

from sqlalchemy.orm import registry, Mapped, mapped_column
from sqlalchemy import  func, DateTime

table_registre =registry()

@table_registre.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    update_at: Mapped[datetime] = mapped_column(DateTime, init=False, nullable=False,
                                                 default=func.now(), onupdate=func.now())

    