"""Configuration de l'application, lue UNIQUEMENT depuis les variables d'environnement.

Aucune valeur sensible n'est écrite ici (risque 3 du T1) : DATABASE_URL contient
le mot de passe de la base et doit être fourni par l'environnement
(.env en local, GitHub Secrets / Environments en CI/CD).
"""
import json
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


def get_producer_tokens() -> dict[str, str]:
    """Retourne la correspondance jeton secret -> producteur.

    Le jeton est fourni par l'environnement et n'est jamais transmis dans le
    corps de la requête. Exemple local : {"token-demo": "Rucher du Lac"}.
    """
    raw_tokens = os.getenv("STOCK_PRODUCER_TOKENS", "")
    if not raw_tokens:
        return {}
    try:
        tokens = json.loads(raw_tokens)
    except json.JSONDecodeError as exc:
        raise RuntimeError("STOCK_PRODUCER_TOKENS doit être un objet JSON valide") from exc
    if not isinstance(tokens, dict) or not all(
        isinstance(token, str) and isinstance(producer, str)
        for token, producer in tokens.items()
    ):
        raise RuntimeError("STOCK_PRODUCER_TOKENS doit mapper des jetons vers des producteurs")
    return tokens
