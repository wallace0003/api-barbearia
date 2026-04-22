from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Client(Base):
    __tablename__ = "clients"

    id_client: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    number: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    schedulings: Mapped[list["Scheduling"]] = relationship(
        "Scheduling",
        back_populates="client",
        cascade="all, delete-orphan",
    )
