from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .enums import PaymentMethod, PaymentStatus


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        UniqueConstraint("id_scheduling", name="uq_payments_id_scheduling"),
    )

    id_payment: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_scheduling: Mapped[int] = mapped_column(
        ForeignKey("schedulings.id_scheduling", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod, name="payment_method"),
        nullable=False,
    )
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.PENDING,
        server_default=PaymentStatus.PENDING.value,
    )

    scheduling: Mapped["Scheduling"] = relationship(
        "Scheduling",
        back_populates="payment",
    )
