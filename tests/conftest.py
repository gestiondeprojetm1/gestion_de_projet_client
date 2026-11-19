"""Configuration des tests : base SQLite en mémoire, sans PostgreSQL."""
import os

# Doit être défini AVANT d'importer l'application (aucun secret nécessaire en CI).
os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
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
            Product(name="Miel Bio", price=8.50, producer="Rucher du Lac"),
            Product(name="Cidre Fermier", price=4.20, producer="Ferme Martin"),
            Product(name="Beurre Local", price=3.10, producer="Maison Dubois"),
        ])
        db.commit()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
