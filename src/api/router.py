from fastapi import APIRouter
from src.api.v1.client import router as client_router
from src.api.v1.barber import router as barber_router
from src.api.v1.cost import router as cost_router
from src.api.v1.payment import router as payment_router
from src.api.v1.service import router as service_router
from src.api.v1.scheduling import router as scheduling_router
from src.api.v1.financial_report import router as financial_report_router


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

api_router.include_router(
    payment_router,
    prefix="/payments",
    tags=["Payments"]
)

api_router.include_router(
    service_router,
    prefix="/services",
    tags=["Services"]
)

api_router.include_router(
    scheduling_router,
    prefix="/schedulings",
    tags=["Schedulings"]
)

api_router.include_router(
    financial_report_router,
    prefix="/financial",
    tags=["Financial Report"]
)
