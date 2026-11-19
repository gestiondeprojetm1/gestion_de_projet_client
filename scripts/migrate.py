"""Applique les migrations SQL versionnées sur la base configurée."""
from pathlib import Path

from app.database import engine


def main() -> None:
    migrations_dir = Path(__file__).resolve().parents[1] / "migrations"
    for migration in sorted(migrations_dir.glob("*.sql")):
        print(f"Application de {migration.name}")
        with engine.begin() as connection:
            connection.exec_driver_sql(migration.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
