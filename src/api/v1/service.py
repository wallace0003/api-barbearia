from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_service_service
from src.schemas.service import (
    ServiceCreate,
    ServiceResponse,
    ServiceUpdate,
)
from src.services.service_service import ServiceService


router = APIRouter(prefix="/services", tags=["Services"])


@router.post(
    path="/",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_service(
    body: ServiceCreate,
    service: ServiceService = Depends(get_service_service),
) -> ServiceResponse:
    return service.create_service(body)


@router.get(
    path="/",
    response_model=list[ServiceResponse],
)
async def list_services(
    service: ServiceService = Depends(get_service_service),
) -> list[ServiceResponse]:
    return service.list_services()


@router.get(
    path="/{id_service}",
    response_model=ServiceResponse,
)
async def get_service(
    id_service: int,
    service: ServiceService = Depends(get_service_service),
) -> ServiceResponse:
    return service.get_service_by_id(id_service)


@router.put(
    path="/{id_service}",
    response_model=ServiceResponse,
)
async def update_service(
    id_service: int,
    body: ServiceUpdate,
    service: ServiceService = Depends(get_service_service),
) -> ServiceResponse:
    return service.update_service(id_service, body)


@router.patch(
    path="/{id_service}",
    response_model=ServiceResponse,
)
async def partial_update_service(
    id_service: int,
    body: ServiceUpdate,
    service: ServiceService = Depends(get_service_service),
) -> ServiceResponse:
    return service.update_service(id_service, body)


@router.delete(
    path="/{id_service}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_service(
    id_service: int,
    service: ServiceService = Depends(get_service_service),
) -> None:
    service.delete_service(id_service)
