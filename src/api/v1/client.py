from fastapi import APIRouter, Depends, status
from src.api.dependencies import get_client_service
from src.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from src.services.client_service import ClientService


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post(
    path="/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_client(
    body: ClientCreate,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    return client_service.create_client(client_data=body)


@router.get(
    path="/",
    response_model=list[ClientResponse],
    status_code=status.HTTP_200_OK,
)
async def get_clients(
    client_service: ClientService = Depends(get_client_service),
) -> list[ClientResponse]:
    return client_service.get_clients()


@router.get(
    path="/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
)
async def get_client_by_id(
    client_id: int,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    return client_service.get_client_by_id(client_id=client_id)


@router.put(
    path="/{client_id}",
    response_model=ClientResponse,
    status_code=status.HTTP_200_OK,
)
async def update_client(
    client_id: int,
    body: ClientUpdate,
    client_service: ClientService = Depends(get_client_service),
) -> ClientResponse:
    return client_service.update_client(
        client_id=client_id,
        client_data=body,
    )


@router.delete(
    path="/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_client(
    client_id: int,
    client_service: ClientService = Depends(get_client_service),
) -> None:
    client_service.delete_client(client_id=client_id)
