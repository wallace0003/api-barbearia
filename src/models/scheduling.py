from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import SchedulingStatus


class Scheduling(Base):
    __tablename__ = "schedulings"
    __table_args__ = (
        Index("ix_schedulings_start_at", "start_at"),
        Index("ix_schedulings_barber_start_at", "id_barber", "start_at"),
    )

    id_scheduling: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_client: Mapped[int] = mapped_column(
        ForeignKey("clients.id_client", ondelete="CASCADE"),
        nullable=False,
    )
    id_barber: Mapped[int] = mapped_column(
        ForeignKey("barbers.id_barber", ondelete="RESTRICT"),
        nullable=False,
    )
    id_service: Mapped[int] = mapped_column(
        ForeignKey("services.id_service", ondelete="RESTRICT"),
        nullable=False,
    )

    status: Mapped[SchedulingStatus] = mapped_column(
        Enum(SchedulingStatus, name="scheduling_status"),
        nullable=False,
        default=SchedulingStatus.PENDING,
        server_default=SchedulingStatus.PENDING.value,
    )

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    client: Mapped["Client"] = relationship(
        "Client",
        back_populates="schedulings",
    )
    barber: Mapped["Barber"] = relationship(
        "Barber",
        back_populates="schedulings",
    )
    service: Mapped["Service"] = relationship(
        "Service",
        back_populates="schedulings",
    )
    payment: Mapped["Payment"] = relationship(
        "Payment",
        back_populates="scheduling",
        uselist=False,
        cascade="all, delete-orphan",
    )
