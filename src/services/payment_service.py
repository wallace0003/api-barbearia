from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.payment import Payment
from src.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentService:
    def __init__(self, session: Session):
        self.session = session

    def create_payment(self, payment_data: PaymentCreate) -> Payment:
        try:
            payment = Payment(**payment_data.model_dump())

            self.session.add(payment)
            self.session.commit()
            self.session.refresh(payment)

            return payment

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Pagamento já existe para este agendamento.",
            )

    def get_payment_by_id(self, id_payment: int) -> Payment:
        payment = self.session.get(Payment, id_payment)

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pagamento não encontrado.",
            )

        return payment

    def list_payments(self) -> list[Payment]:
        return self.session.query(Payment).all()

    def update_payment(self, id_payment: int, payment_data: PaymentUpdate) -> Payment:
        payment = self.get_payment_by_id(id_payment)

        data = payment_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(payment, field, value)

        self.session.commit()
        self.session.refresh(payment)

        return payment

    def delete_payment(self, id_payment: int) -> None:
        payment = self.get_payment_by_id(id_payment)

        self.session.delete(payment)
        self.session.commit()
    