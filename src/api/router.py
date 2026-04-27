from fastapi import APIRouter
from src.api.v1.client import router as client_router


api_router = APIRouter()

api_router.include_router(
    client_router,
    prefix="/clients",
    tags=["Clients"],
)
