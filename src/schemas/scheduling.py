from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from models.enums import SchedulingStatus


class SchedulingBase(BaseModel):
    id_client: int
    id_barber: int
    id_service: int
    status: SchedulingStatus = SchedulingStatus.PENDING
    start_at: datetime
    end_at: datetime


class SchedulingCreate(SchedulingBase):
    pass


class SchedulingUpdate(BaseModel):
    id_client: int | None = None
    id_barber: int | None = None
    id_service: int | None = None
    status: SchedulingStatus | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


class SchedulingResponse(SchedulingBase):
    model_config = ConfigDict(from_attributes=True)

    id_scheduling: int
