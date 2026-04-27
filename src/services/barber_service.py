from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.barber import Barber
from src.schemas.barber import BarberCreate, BarberUpdate


class BarberService:
    def __init__(self, session: Session):
        self.session = session

    def create_barber(self, barber_data: BarberCreate) -> Barber:
        try:
            barber = Barber(**barber_data.model_dump())

            self.session.add(barber)
            self.session.commit()
            self.session.refresh(barber)

            return barber

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um barbeiro com este e-mail.",
            )

    def get_barber_by_id(self, id_barber: int) -> Barber:
        barber = self.session.get(Barber, id_barber)

        if not barber:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Barbeiro não encontrado.",
            )

        return barber

    def list_barbers(self) -> list[Barber]:
        return self.session.query(Barber).all()

    def update_barber(self, id_barber: int, barber_data: BarberUpdate) -> Barber:
        barber = self.get_barber_by_id(id_barber)

        data = barber_data.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(barber, field, value)

        try:
            self.session.commit()
            self.session.refresh(barber)
            return barber

        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um barbeiro com este e-mail.",
            )

    def delete_barber(self, id_barber: int) -> None:
        barber = self.get_barber_by_id(id_barber)

        self.session.delete(barber)
        self.session.commit()
