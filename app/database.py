"""Connexion à la base de données (SQLAlchemy)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_database_url

engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Classe de base des modèles. Base.metadata servira de cible à Alembic."""


def get_db():
    """Dépendance FastAPI : ouvre une session par requête puis la ferme."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crée les tables au démarrage.

    Partie 2 (gestion du stock, risque 5 du T1) : cette fonction sera remplacée
    par des migrations Alembic (`alembic upgrade head`), testées en staging
    avant la production. Les modèles sont déjà isolés dans app/models.py.
    """
    from app import models  # noqa: F401  (enregistre les tables dans Base.metadata)

    Base.metadata.create_all(bind=engine)
