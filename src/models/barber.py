from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Barber(Base):
    __tablename__ = "barbers"

    id_barber: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    barber_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    number: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    schedulings: Mapped[list["Scheduling"]] = relationship(
        "Scheduling",
        back_populates="barber",
    )
