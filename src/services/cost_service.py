from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.cost import Cost
from schemas.cost_schema import CostCreate, CostUpdate


class CostService:
    def __init__(self, session: Session):
        self.session = session

    def create_cost(self, cost_data: CostCreate) -> Cost:
        cost = Cost(**cost_data.model_dump())

        self.session.add(cost)
        self.session.commit()
        self.session.refresh(cost)

        return cost

    def get_cost_by_id(self, id_costs: int) -> Cost:
        cost = self.session.get(Cost, id_costs)

        if not cost:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Custo não encontrado.",
            )

        return cost

    def list_costs(self) -> list[Cost]:
        return self.session.query(Cost).all()

    def update_cost(self, id_costs: int, cost_data: CostUpdate) -> Cost:
        cost = self.get_cost_by_id(id_costs)

        data = cost_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(cost, field, value)

        self.session.commit()
        self.session.refresh(cost)

        return cost

    def delete_cost(self, id_costs: int) -> None:
        cost = self.get_cost_by_id(id_costs)

        self.session.delete(cost)
        self.session.commit()
