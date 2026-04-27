from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.client import Client
from src.schemas.client import ClientCreate, ClientUpdate


class ClientService:
    def __init__(self, session: Session):
        self.session = session

    def create_client(self, client_data: ClientCreate) -> Client:
        try:
            client = Client(
                client_name=client_data.client_name,
                email=client_data.email,
                number=client_data.number,
            )

            self.session.add(client)
            self.session.commit()
            self.session.refresh(client)

            return client

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um cliente com este e-mail.",
            )

    def get_clients(self) -> list[Client]:
        return self.session.query(Client).all()

    def get_client_by_id(self, client_id: int) -> Client:
        client = self.session.get(Client, client_id)

        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado.",
            )

        return client

    def update_client(self, client_id: int, client_data: ClientUpdate) -> Client:
        client = self.get_client_by_id(client_id)

        data = client_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(client, field, value)

        try:
            self.session.commit()
            self.session.refresh(client)

            return client

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um cliente com este e-mail.",
            )

    def delete_client(self, client_id: int) -> None:
        client = self.get_client_by_id(client_id)

        self.session.delete(client)
        self.session.commit()
