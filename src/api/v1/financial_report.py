from datetime import date

from fastapi import APIRouter, Depends, Query, status

from src.api.dependencies import get_financial_report_service
from src.schemas.financial_report import FinancialReportResponse
from src.services.financial_report_service import FinancialReportService


router = APIRouter()


@router.get(
    path="/profit",
    response_model=FinancialReportResponse,
    status_code=status.HTTP_200_OK,
)
async def get_profit_by_period(
    start_date: date = Query(
        ...,
        description="Data inicial do período. Formato: YYYY-MM-DD.",
        examples=["2026-05-01"],
    ),
    end_date: date = Query(
        ...,
        description="Data final do período. Formato: YYYY-MM-DD.",
        examples=["2026-05-31"],
    ),
    service: FinancialReportService = Depends(get_financial_report_service),
) -> FinancialReportResponse:
    return service.get_profit_by_period(
        start_date=start_date,
        end_date=end_date,
    )
