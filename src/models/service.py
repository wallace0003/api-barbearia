from decimal import Decimal

from sqlalchemy import Boolean, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Service(Base):
    __tablename__ = "services"

    id_service: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    service_name: Mapped[str] = mapped_column(String(60), nullable=False, unique=True, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)  # em minutos
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    schedulings: Mapped[list["Scheduling"]] = relationship(
        "Scheduling",
        back_populates="service",
    )
