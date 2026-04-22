from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from models import Base


class Database:
    """
    Gerenciador genérico de banco de dados com SQLAlchemy ORM.

    Compatível com qualquer banco suportado pelo SQLAlchemy.

    Exemplos de URL:
    - SQLite:
      sqlite:///./barbearia.db

    - PostgreSQL:
      postgresql+psycopg2://user:password@localhost:5432/barbearia

    - MySQL:
      mysql+pymysql://user:password@localhost:3306/barbearia
    """

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        **engine_kwargs: Any,
    ) -> None:
        self.database_url = database_url
        self.echo = echo

        default_engine_kwargs = {
            "echo": echo,
            "future": True,
            "pool_pre_ping": True,
        }

        if not database_url.startswith("sqlite"):
            default_engine_kwargs.update(
                {
                    "pool_recycle": 1800,
                }
            )
        else:
            # SQLite precisa disso em alguns cenários
            default_engine_kwargs.update(
                {
                    "connect_args": {"check_same_thread": False},
                }
            )

        default_engine_kwargs.update(engine_kwargs)

        self.engine: Engine = create_engine(
            self.database_url,
            **default_engine_kwargs,
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=Session,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as exc:
            print(f"Erro ao conectar com o banco: {exc}")
            return False

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Context manager para sessão com commit/rollback automáticos.

        Exemplo:
            with db.session() as session:
                session.add(obj)
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        """
        Retorna uma sessão manual.
        Use quando quiser controlar commit/rollback externamente.
        """
        return self.SessionLocal()

    def get_db(self) -> Generator[Session, None, None]:
        """
        Dependência para FastAPI.

        Exemplo:
            def route(db: Session = Depends(database.get_db)):
                ...
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def dispose(self) -> None:
        self.engine.dispose()
