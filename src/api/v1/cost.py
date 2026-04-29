from fastapi import APIRouter, Depends, status
from src.api.dependencies import get_cost_service
from src.schemas.cost import CostCreate, CostResponse, CostUpdate
from src.services.cost_service import CostService


router = APIRouter(prefix="/costs", tags=["Costs"])


@router.post(
    path="/",
    response_model=CostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cost(
    body: CostCreate,
    cost_service: CostService = Depends(get_cost_service),
) -> CostResponse:
    return cost_service.create_cost(cost_data=body)


@router.get(
    path="/",
    response_model=list[CostResponse],
    status_code=status.HTTP_200_OK,
)
async def list_costs(
    cost_service: CostService = Depends(get_cost_service),
) -> list[CostResponse]:
    return cost_service.list_costs()


@router.get(
    path="/{id_costs}",
    response_model=CostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_cost_by_id(
    id_costs: int,
    cost_service: CostService = Depends(get_cost_service),
) -> CostResponse:
    return cost_service.get_cost_by_id(id_costs=id_costs)


@router.put(
    path="/{id_costs}",
    response_model=CostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_cost(
    id_costs: int,
    body: CostUpdate,
    cost_service: CostService = Depends(get_cost_service),
) -> CostResponse:
    return cost_service.update_cost(
        id_costs=id_costs,
        cost_data=body,
    )


@router.patch(
    path="/{id_costs}",
    response_model=CostResponse,
    status_code=status.HTTP_200_OK,
)
async def partial_update_cost(
    id_costs: int,
    body: CostUpdate,
    cost_service: CostService = Depends(get_cost_service),
) -> CostResponse:
    return cost_service.update_cost(
        id_costs=id_costs,
        cost_data=body,
    )


@router.delete(
    path="/{id_costs}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_cost(
    id_costs: int,
    cost_service: CostService = Depends(get_cost_service),
) -> None:
    cost_service.delete_cost(id_costs=id_costs)
