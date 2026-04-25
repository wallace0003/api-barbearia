from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=0)
    duration_minutes: int = Field(gt=0)
    active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    duration_minutes: int | None = Field(default=None, gt=0)
    active: bool | None = None


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime