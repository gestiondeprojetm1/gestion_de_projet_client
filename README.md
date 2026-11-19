# gestion_de_projet_client

## Lancer le projet en local

Prérequis : Docker et Docker Compose.

1. Créer le fichier de configuration local (valeurs factices, jamais versionné) :

   ```bash
   cp .env.example .env
   ```

2. Construire et démarrer l'API et la base PostgreSQL :

   ```bash
   docker compose up --build
   ```

3. Dans un autre terminal, insérer les 1 200 produits de démonstration (vous pouvez relancer la commande sans risque : les produits ne sont pas dupliqués) :

   ```bash
   docker compose run --rm api python scripts/seed.py
   ```

4. Lancer les tests (base SQLite en mémoire, PostgreSQL n'est pas nécessaire) :

   ```bash
   pip install -r requirements-dev.txt
   pytest -v
   ```

5. Ouvrir la documentation Swagger : <http://localhost:8000/docs>

   Vérifier la version déployée : <http://localhost:8000/health>
