"""Configuration de l'application, lue UNIQUEMENT depuis les variables d'environnement.

Aucune valeur sensible n'est écrite ici (risque 3 du T1) : DATABASE_URL contient
le mot de passe de la base et doit être fourni par l'environnement
(.env en local, GitHub Secrets / Environments en CI/CD).
"""
import os


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "La variable d'environnement DATABASE_URL n'est pas définie. "
            "Copiez .env.example en .env (voir README)."
        )
    return url


# Version déployée, affichée dans /health (risque 2 du T1).
# Valeurs par défaut non sensibles, utilisées seulement en développement.
APP_VERSION = os.getenv("APP_VERSION", "dev")
GIT_SHA = os.getenv("GIT_SHA", "unknown")
