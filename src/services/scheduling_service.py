from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.barber import Barber
from src.models.client import Client
from src.models.scheduling import Scheduling
from src.models.service import Service
from src.schemas.scheduling import SchedulingCreate, SchedulingUpdate


class SchedulingService:
    def __init__(self, session: Session):
        self.session = session

    def create_scheduling(self, scheduling_data: SchedulingCreate) -> Scheduling:
        self._validate_relations(scheduling_data)
        self._validate_barber_availability(
            id_barber=scheduling_data.id_barber,
            start_at=scheduling_data.start_at,
            end_at=scheduling_data.end_at,
        )

        scheduling = Scheduling(**scheduling_data.model_dump())

        self.session.add(scheduling)
        self.session.commit()
        self.session.refresh(scheduling)

        return scheduling

    def get_scheduling_by_id(self, id_scheduling: int) -> Scheduling:
        scheduling = self.session.get(Scheduling, id_scheduling)

        if not scheduling:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agendamento não encontrado.",
            )

        return scheduling

    def list_schedulings(self) -> list[Scheduling]:
        return self.session.query(Scheduling).all()

    def update_scheduling(
        self,
        id_scheduling: int,
        scheduling_data: SchedulingUpdate,
    ) -> Scheduling:
        scheduling = self.get_scheduling_by_id(id_scheduling)

        data = scheduling_data.model_dump(exclude_unset=True)

        new_id_barber = data.get("id_barber", scheduling.id_barber)
        new_start_at = data.get("start_at", scheduling.start_at)
        new_end_at = data.get("end_at", scheduling.end_at)

        if "id_client" in data or "id_barber" in data or "id_service" in data:
            self._validate_relations_for_update(
                id_client=data.get("id_client"),
                id_barber=data.get("id_barber"),
                id_service=data.get("id_service"),
            )

        if "id_barber" in data or "start_at" in data or "end_at" in data:
            self._validate_barber_availability(
                id_barber=new_id_barber,
                start_at=new_start_at,
                end_at=new_end_at,
                ignore_id_scheduling=id_scheduling,
            )

        for field, value in data.items():
            setattr(scheduling, field, value)

        self.session.commit()
        self.session.refresh(scheduling)

        return scheduling

    def delete_scheduling(self, id_scheduling: int) -> None:
        scheduling = self.get_scheduling_by_id(id_scheduling)

        self.session.delete(scheduling)
        self.session.commit()

    def _validate_relations(self, scheduling_data: SchedulingCreate) -> None:
        if not self.session.get(Client, scheduling_data.id_client):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado.",
            )

        if not self.session.get(Barber, scheduling_data.id_barber):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Barbeiro não encontrado.",
            )

        if not self.session.get(Service, scheduling_data.id_service):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado.",
            )

    def _validate_relations_for_update(
        self,
        id_client: int | None = None,
        id_barber: int | None = None,
        id_service: int | None = None,
    ) -> None:
        if id_client is not None and not self.session.get(Client, id_client):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado.",
            )

        if id_barber is not None and not self.session.get(Barber, id_barber):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Barbeiro não encontrado.",
            )

        if id_service is not None and not self.session.get(Service, id_service):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado.",
            )

    def _validate_barber_availability(
        self,
        id_barber: int,
        start_at,
        end_at,
        ignore_id_scheduling: int | None = None,
    ) -> None:
        if start_at >= end_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O horário de início deve ser menor que o horário de fim.",
            )

        query = self.session.query(Scheduling).filter(
            Scheduling.id_barber == id_barber,
            Scheduling.start_at < end_at,
            Scheduling.end_at > start_at,
        )

        if ignore_id_scheduling is not None:
            query = query.filter(Scheduling.id_scheduling != ignore_id_scheduling)

        exists_conflict = query.first()

        if exists_conflict:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este barbeiro já possui um agendamento neste horário.",
            )
