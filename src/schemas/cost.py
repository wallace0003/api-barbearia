# src/schemas/cost.py

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CostBase(BaseModel):
    description: str = Field(min_length=2, max_length=100)
    price: Decimal = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)


class CostCreate(CostBase):
    pass


class CostUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=2, max_length=100)
    price: Decimal | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=2, max_length=50)


class CostResponse(CostBase):
    model_config = ConfigDict(from_attributes=True)
    id_costs: int
