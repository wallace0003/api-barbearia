from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_barber_service
from src.schemas.barber import BarberCreate, BarberResponse, BarberUpdate
from src.services.barber_service import BarberService


router = APIRouter(prefix="/barbers", tags=["Barbers"])


@router.post(
    path="/",
    response_model=BarberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_barber(
    body: BarberCreate,
    barber_service: BarberService = Depends(get_barber_service),
) -> BarberResponse:
    return barber_service.create_barber(barber_data=body)


@router.get(
    path="/",
    response_model=list[BarberResponse],
    status_code=status.HTTP_200_OK,
)
async def list_barbers(
    barber_service: BarberService = Depends(get_barber_service),
) -> list[BarberResponse]:
    return barber_service.list_barbers()


@router.get(
    path="/{id_barber}",
    response_model=BarberResponse,
    status_code=status.HTTP_200_OK,
)
async def get_barber_by_id(
    id_barber: int,
    barber_service: BarberService = Depends(get_barber_service),
) -> BarberResponse:
    return barber_service.get_barber_by_id(id_barber=id_barber)


@router.put(
    path="/{id_barber}",
    response_model=BarberResponse,
    status_code=status.HTTP_200_OK,
)
async def update_barber(
    id_barber: int,
    body: BarberUpdate,
    barber_service: BarberService = Depends(get_barber_service),
) -> BarberResponse:
    return barber_service.update_barber(
        id_barber=id_barber,
        barber_data=body,
    )


@router.patch(
    path="/{id_barber}",
    response_model=BarberResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_barber(
    id_barber: int,
    body: BarberUpdate,
    barber_service: BarberService = Depends(get_barber_service),
) -> BarberResponse:
    return barber_service.update_barber(
        id_barber=id_barber,
        barber_data=body,
    )


@router.delete(
    path="/{id_barber}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_barber(
    id_barber: int,
    barber_service: BarberService = Depends(get_barber_service),
) -> None:
    barber_service.delete_barber(id_barber=id_barber)
