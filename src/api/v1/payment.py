from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_payment_service
from src.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentUpdate,
)
from src.services.payment_service import PaymentService


router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post(
    path="/",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    body: PaymentCreate,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return service.create_payment(payment_data=body)


@router.get(
    path="/",
    response_model=list[PaymentResponse],
)
async def list_payments(
    service: PaymentService = Depends(get_payment_service),
) -> list[PaymentResponse]:
    return service.list_payments()


@router.get(
    path="/{id_payment}",
    response_model=PaymentResponse,
)
async def get_payment(
    id_payment: int,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return service.get_payment_by_id(id_payment)


@router.put(
    path="/{id_payment}",
    response_model=PaymentResponse,
)
async def update_payment(
    id_payment: int,
    body: PaymentUpdate,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return service.update_payment(id_payment, body)


@router.patch(
    path="/{id_payment}",
    response_model=PaymentResponse,
)
async def partial_update_payment(
    id_payment: int,
    body: PaymentUpdate,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    return service.update_payment(id_payment, body)


@router.delete(
    path="/{id_payment}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_payment(
    id_payment: int,
    service: PaymentService = Depends(get_payment_service),
) -> None:
    service.delete_payment(id_payment)
