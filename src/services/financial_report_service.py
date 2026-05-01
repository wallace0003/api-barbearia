from calendar import monthrange
from datetime import date, datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src.models.cost import Cost
from src.models.scheduling import Scheduling
from src.schemas.financial_report import (
    FinancialReportCostItem,
    FinancialReportCostSummary,
    FinancialReportPeriod,
    FinancialReportResponse,
    FinancialReportRevenueItem,
    FinancialReportSummary,
)


class FinancialReportService:
    def __init__(self, session: Session):
        self.session = session

    def _to_money(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def _count_days_in_period(self, start_date: date, end_date: date) -> int:
        return (end_date - start_date).days + 1

    def _calculate_proportional_monthly_cost(
        self,
        monthly_price: Decimal,
        start_date: date,
        end_date: date,
    ) -> Decimal:
        total = Decimal("0.00")
        current_date = start_date

        while current_date <= end_date:
            days_in_month = monthrange(current_date.year, current_date.month)[1]

            last_day_of_current_month = date(
                current_date.year,
                current_date.month,
                days_in_month,
            )

            period_end_in_current_month = min(end_date, last_day_of_current_month)

            days_used_in_month = (
                period_end_in_current_month - current_date
            ).days + 1

            daily_cost = monthly_price / Decimal(days_in_month)
            total += daily_cost * Decimal(days_used_in_month)

            current_date = period_end_in_current_month + timedelta(days=1)

        return self._to_money(total)

    def get_profit_by_period(
        self,
        start_date: date,
        end_date: date,
    ) -> FinancialReportResponse:
        if end_date < start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_date deve ser maior ou igual a start_date.",
            )

        start_datetime = datetime.combine(start_date, time.min)

        # Final exclusivo para pegar o end_date inteiro.
        end_datetime = datetime.combine(end_date + timedelta(days=1), time.min)

        schedulings = (
            self.session.query(Scheduling)
            .options(
                joinedload(Scheduling.client),
                joinedload(Scheduling.barber),
                joinedload(Scheduling.service),
            )
            .filter(
                Scheduling.start_at >= start_datetime,
                Scheduling.start_at < end_datetime,
            )
            .all()
        )

        costs = self.session.query(Cost).all()

        revenues: list[FinancialReportRevenueItem] = []
        total_revenue = Decimal("0.00")

        for scheduling in schedulings:
            service = scheduling.service
            client = scheduling.client
            barber = scheduling.barber

            service_price = service.price if service else Decimal("0.00")
            total_revenue += service_price

            revenues.append(
                FinancialReportRevenueItem(
                    id_scheduling=scheduling.id_scheduling,
                    start_at=scheduling.start_at,
                    end_at=scheduling.end_at,
                    service_name=(
                        service.service_name if service else "Serviço não informado"
                    ),
                    service_price=self._to_money(service_price),
                    barber_name=(
                        barber.barber_name if barber else None
                    ),
                    client_name=(
                        client.client_name if client else None
                    ),
                )
            )

        cost_items: list[FinancialReportCostItem] = []
        monthly_total_costs = Decimal("0.00")
        proportional_total_costs = Decimal("0.00")

        for cost in costs:
            monthly_total_costs += cost.price

            proportional_price = self._calculate_proportional_monthly_cost(
                monthly_price=cost.price,
                start_date=start_date,
                end_date=end_date,
            )

            proportional_total_costs += proportional_price

            cost_items.append(
                FinancialReportCostItem(
                    id_costs=cost.id_costs,
                    description=cost.description,
                    category=cost.category,
                    monthly_price=self._to_money(cost.price),
                    proportional_price=self._to_money(proportional_price),
                )
            )

        total_revenue = self._to_money(total_revenue)
        monthly_total_costs = self._to_money(monthly_total_costs)
        proportional_total_costs = self._to_money(proportional_total_costs)

        net_profit = self._to_money(total_revenue - proportional_total_costs)

        return FinancialReportResponse(
            period=FinancialReportPeriod(
                start_date=start_date,
                end_date=end_date,
                days_in_period=self._count_days_in_period(
                    start_date=start_date,
                    end_date=end_date,
                ),
            ),
            summary=FinancialReportSummary(
                total_revenue=total_revenue,
                total_costs=proportional_total_costs,
                net_profit=net_profit,
                total_schedulings=len(schedulings),
                total_cost_items=len(costs),
            ),
            costs_summary=FinancialReportCostSummary(
                monthly_total_costs=monthly_total_costs,
                proportional_total_costs=proportional_total_costs,
                allocation_method="PRORATED_BY_DAYS",
            ),
            revenues=revenues,
            costs=cost_items,
        )
