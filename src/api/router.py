from fastapi import APIRouter
from src.api.v1.client import router as client_router
from src.api.v1.barber import router as barber_router
from src.api.v1.cost import router as cost_router


api_router = APIRouter()

api_router.include_router(
    client_router,
    prefix="/clients",
    tags=["Clients"],
)

api_router.include_router(
    barber_router,
    prefix="/barbers",
    tags=["Barbers"]
)



api_router.include_router(
    cost_router,
    prefix="/costs",
    tags=["Costs"]
)
