from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator

from src.models.enums import SchedulingStatus


class SchedulingBase(BaseModel):
    id_client: int
    id_barber: int
    id_service: int
    start_at: datetime
    end_at: datetime
    status: SchedulingStatus = SchedulingStatus.PENDING

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_at <= self.start_at:
            raise ValueError("end_at deve ser maior que start_at.")
        return self


class SchedulingCreate(SchedulingBase):
    pass


class SchedulingUpdate(BaseModel):
    id_client: int | None = None
    id_barber: int | None = None
    id_service: int | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    status: SchedulingStatus | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValueError("end_at deve ser maior que start_at.")
        return self


class SchedulingClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_client: int
    client_name: str
    email: str
    number: str


class SchedulingBarberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_barber: int
    barber_name: str
    email: str
    number: str


class SchedulingServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_service: int
    service_name: str
    price: Decimal
    duration: int


class SchedulingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_scheduling: int
    id_client: int
    id_barber: int
    id_service: int
    start_at: datetime
    end_at: datetime
    status: SchedulingStatus

    client: SchedulingClientResponse
    barber: SchedulingBarberResponse
    service: SchedulingServiceResponse
