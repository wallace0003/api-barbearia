from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class BarberBase(BaseModel):
    barber_name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    number: str = Field(min_length=10, max_length=11)
    status: bool = True


class BarberCreate(BarberBase):
    pass


class BarberUpdate(BaseModel):
    barber_name: str | None = Field(default=None, min_length=2, max_length=60)
    email: EmailStr | None = None
    number: str | None = Field(default=None, min_length=10, max_length=11)
    status: bool | None = None


class BarberResponse(BarberBase):
    model_config = ConfigDict(from_attributes=True)

    id_barber: int
    created_at: datetime
