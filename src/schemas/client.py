from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientBase(BaseModel):
    client_name: str = Field(min_length=2, max_length=60)
    email: EmailStr
    number: str = Field(min_length=10, max_length=11)


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    client_name: str | None = Field(default=None, min_length=2, max_length=60)
    email: EmailStr | None = None
    number: str | None = Field(default=None, min_length=10, max_length=11)


class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id_client: int
    created_at: datetime
