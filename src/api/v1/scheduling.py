from fastapi import APIRouter, Depends, status

from src.api.dependencies import get_scheduling_service
from src.schemas.scheduling import (
    SchedulingCreate,
    SchedulingResponse,
    SchedulingUpdate,
)
from src.services.scheduling_service import SchedulingService


router = APIRouter(prefix="/schedulings", tags=["Schedulings"])


@router.post(
    path="/",
    response_model=SchedulingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_scheduling(
    body: SchedulingCreate,
    service: SchedulingService = Depends(get_scheduling_service),
) -> SchedulingResponse:
    return service.create_scheduling(body)


@router.get(
    path="/",
    response_model=list[SchedulingResponse],
    status_code=status.HTTP_200_OK,
)
async def list_schedulings(
    service: SchedulingService = Depends(get_scheduling_service),
) -> list[SchedulingResponse]:
    return service.list_schedulings()


@router.get(
    path="/{id_scheduling}",
    response_model=SchedulingResponse,
    status_code=status.HTTP_200_OK,
)
async def get_scheduling_by_id(
    id_scheduling: int,
    service: SchedulingService = Depends(get_scheduling_service),
) -> SchedulingResponse:
    return service.get_scheduling_by_id(id_scheduling)


@router.put(
    path="/{id_scheduling}",
    response_model=SchedulingResponse,
    status_code=status.HTTP_200_OK,
)
async def update_scheduling(
    id_scheduling: int,
    body: SchedulingUpdate,
    service: SchedulingService = Depends(get_scheduling_service),
) -> SchedulingResponse:
    return service.update_scheduling(id_scheduling, body)


@router.patch(
    path="/{id_scheduling}",
    response_model=SchedulingResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_scheduling(
    id_scheduling: int,
    body: SchedulingUpdate,
    service: SchedulingService = Depends(get_scheduling_service),
) -> SchedulingResponse:
    return service.update_scheduling(id_scheduling, body)


@router.delete(
    path="/{id_scheduling}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_scheduling(
    id_scheduling: int,
    service: SchedulingService = Depends(get_scheduling_service),
) -> None:
    service.delete_scheduling(id_scheduling)
