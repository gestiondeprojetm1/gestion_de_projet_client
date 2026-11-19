# Release initiale — préparation D2.1

Cette release décrit la base technique avant la mise en production effective.

- Fonctionnalité : déclaration et consommation atomique du stock.
- Image : à publier par le workflow sur GHCR avec un tag SemVer et le SHA du commit.
- Migration : `migrations/001_add_stock.sql`, additive et sans suppression de données.
- Vérifications attendues : pytest, build Docker, test PostgreSQL de concurrence et smoke test `/health`.
- D2.2 reste responsable du choix de version, du go/no-go et des déploiements staging/production.
