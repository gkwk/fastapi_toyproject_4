from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, Date, DateTime, ForeignKey, Table, Column, BigInteger, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_database_postgresql.database import Base

if TYPE_CHECKING:
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = {}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP")
    )
    is_banned: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
