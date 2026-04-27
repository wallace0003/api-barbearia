from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.service import Service
from src.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    def __init__(self, session: Session):
        self.session = session

    def create_service(self, service_data: ServiceCreate) -> Service:
        try:
            service = Service(**service_data.model_dump())

            self.session.add(service)
            self.session.commit()
            self.session.refresh(service)

            return service

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um serviço com este nome.",
            )

    def get_service_by_id(self, id_service: int) -> Service:
        service = self.session.get(Service, id_service)

        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado.",
            )

        return service

    def list_services(self) -> list[Service]:
        return self.session.query(Service).all()

    def update_service(self, id_service: int, service_data: ServiceUpdate) -> Service:
        service = self.get_service_by_id(id_service)

        data = service_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(service, field, value)

        try:
            self.session.commit()
            self.session.refresh(service)
            return service

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um serviço com este nome.",
            )

    def delete_service(self, id_service: int) -> None:
        service = self.get_service_by_id(id_service)

        self.session.delete(service)
        self.session.commit()
    