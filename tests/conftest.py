"""Configuration des tests : base SQLite en mémoire, sans PostgreSQL."""
import os

# Doit être défini AVANT d'importer l'application (aucun secret nécessaire en CI).
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault(
    "STOCK_PRODUCER_TOKENS",
    '{"test-rucher-token":"Rucher du Lac","test-ferme-token":"Ferme Martin"}',
)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.exc import IntegrityError  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Product  # noqa: E402

# StaticPool : une seule connexion partagée, donc la même base en mémoire partout.
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSession = sessionmaker(bind=engine, autoflush=False)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestingSession() as db:
        db.add_all([
            Product(name="Miel Bio", price=8.50, producer="Rucher du Lac", stock=10),
            Product(name="Cidre Fermier", price=4.20, producer="Ferme Martin", stock=10),
            Product(name="Beurre Local", price=3.10, producer="Maison Dubois", stock=10),
        ])
        db.commit()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def stock_headers():
    return {"Authorization": "Bearer test-rucher-token"}


@pytest.fixture
def db_session(client):
    with TestingSession() as db:
        yield db


@pytest.fixture
def broken_client():
    class BrokenSession:
        def execute(self, _query):
            raise RuntimeError("PostgreSQL indisponible")

        def rollback(self):
            pass

    def broken_db():
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def integrity_error():
    return IntegrityError
