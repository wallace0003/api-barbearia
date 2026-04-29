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

    def _validate_client_exists(self, id_client: int) -> None:
        if not self.session.get(Client, id_client):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado.",
            )

    def _validate_barber_exists(self, id_barber: int) -> None:
        if not self.session.get(Barber, id_barber):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Barbeiro não encontrado.",
            )

    def _validate_service_exists(self, id_service: int) -> None:
        if not self.session.get(Service, id_service):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Serviço não encontrado.",
            )

    def _validate_schedule_conflict(
        self,
        id_barber: int,
        start_at,
        end_at,
        ignore_id_scheduling: int | None = None,
    ) -> None:
        query = self.session.query(Scheduling).filter(
            Scheduling.id_barber == id_barber,
            Scheduling.start_at < end_at,
            Scheduling.end_at > start_at,
        )

        if ignore_id_scheduling is not None:
            query = query.filter(Scheduling.id_scheduling != ignore_id_scheduling)

        exists = query.first()

        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um agendamento para este barbeiro nesse horário.",
            )

    def create_scheduling(self, scheduling_data: SchedulingCreate) -> Scheduling:
        self._validate_client_exists(scheduling_data.id_client)
        self._validate_barber_exists(scheduling_data.id_barber)
        self._validate_service_exists(scheduling_data.id_service)

        self._validate_schedule_conflict(
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

        id_client = data.get("id_client", scheduling.id_client)
        id_barber = data.get("id_barber", scheduling.id_barber)
        id_service = data.get("id_service", scheduling.id_service)
        start_at = data.get("start_at", scheduling.start_at)
        end_at = data.get("end_at", scheduling.end_at)

        if end_at <= start_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_at deve ser maior que start_at.",
            )

        self._validate_client_exists(id_client)
        self._validate_barber_exists(id_barber)
        self._validate_service_exists(id_service)

        self._validate_schedule_conflict(
            id_barber=id_barber,
            start_at=start_at,
            end_at=end_at,
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
