from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class CostBase(BaseModel):
    cost_name: str = Field(min_length=2, max_length=80)
    value: Decimal = Field(gt=0)
    description: str | None = None
    status: bool = True


class CostCreate(CostBase):
    pass


class CostUpdate(BaseModel):
    cost_name: str | None = Field(default=None, min_length=2, max_length=80)
    value: Decimal | None = Field(default=None, gt=0)
    description: str | None = None
    status: bool | None = None


class CostResponse(CostBase):
    model_config = ConfigDict(from_attributes=True)

    id_costs: int
