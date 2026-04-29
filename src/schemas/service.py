from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ServiceBase(BaseModel):
    service_name: str = Field(min_length=2, max_length=60)
    price: Decimal = Field(gt=0)
    duration: int = Field(gt=0)
    status: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_name: str | None = Field(default=None, min_length=2, max_length=60)
    price: Decimal | None = Field(default=None, gt=0)
    duration: int | None = Field(default=None, gt=0)
    status: bool | None = None


class ServiceResponse(ServiceBase):
    model_config = ConfigDict(from_attributes=True)

    id_service: int
