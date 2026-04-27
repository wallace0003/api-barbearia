from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.engine import Database

from src.services.client_service import ClientService
from src.services.barber_service import BarberService
from src.services.service_service import ServiceService
from src.services.payment_service import PaymentService
from src.services.cost_service import CostService
from src.services.scheduling_service import SchedulingService


DATABASE_URL = "postgresql+psycopg2://barber:barber123@localhost:5433/barber_db"

db = Database(DATABASE_URL, echo=True)


def get_db_session() -> Generator[Session, None, None]:
    with db.get_session() as session:
        yield session


def get_client_service(
    session: Session = Depends(get_db_session),
) -> ClientService:
    return ClientService(session)


def get_employee_service(
    session: Session = Depends(get_db_session),
) -> BarberService:
    return BarberService(session)


def get_service_service(
    session: Session = Depends(get_db_session),
) -> ServiceService:
    return ServiceService(session)


def get_appointment_service(
    session: Session = Depends(get_db_session),
) -> CostService:
    return CostService(session)


def get_payment_service(
    session: Session = Depends(get_db_session),
) -> PaymentService:
    return PaymentService(session)


def get_financial_service(
    session: Session = Depends(get_db_session),
) -> SchedulingService:
    return SchedulingService(session)
