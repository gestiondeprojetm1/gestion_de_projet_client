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

    Les migrations versionnées sont également disponibles dans `migrations/` et
    peuvent être appliquées avec `python scripts/migrate.py` avant un déploiement.
    """
    from app import models  # noqa: F401  (enregistre les tables dans Base.metadata)

    Base.metadata.create_all(bind=engine)
    # Les bases existantes doivent être migrées explicitement avec
    # `python scripts/migrate.py` avant le démarrage. Ainsi create_all() ne
    # concurrence pas une migration de schéma en production.
