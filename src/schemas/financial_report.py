from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class FinancialReportPeriod(BaseModel):
    start_date: date
    end_date: date
    days_in_period: int


class FinancialReportRevenueItem(BaseModel):
    id_scheduling: int
    start_at: datetime
    end_at: datetime
    service_name: str
    service_price: Decimal
    barber_name: str | None = None
    client_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FinancialReportCostItem(BaseModel):
    id_costs: int
    description: str
    category: str
    monthly_price: Decimal
    proportional_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class FinancialReportCostSummary(BaseModel):
    monthly_total_costs: Decimal
    proportional_total_costs: Decimal
    allocation_method: str


class FinancialReportSummary(BaseModel):
    total_revenue: Decimal
    total_costs: Decimal
    net_profit: Decimal
    total_schedulings: int
    total_cost_items: int


class FinancialReportResponse(BaseModel):
    period: FinancialReportPeriod
    summary: FinancialReportSummary
    costs_summary: FinancialReportCostSummary
    revenues: list[FinancialReportRevenueItem]
    costs: list[FinancialReportCostItem]
