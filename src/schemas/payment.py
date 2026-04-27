from pydantic import BaseModel, ConfigDict

from src.models.enums import PaymentMethod, PaymentStatus


class PaymentBase(BaseModel):
    id_scheduling: int
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_method: PaymentMethod | None = None
    status: PaymentStatus | None = None


class PaymentResponse(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id_payment: int
