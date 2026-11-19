# Procédure de rollback préparée pour D2.2

Le workflow publie l'image sous un digest immuable dans `deployment.env`. Le digest de la version précédente doit être conservé dans l'environnement de déploiement ou dans l'artefact de la release précédente.

## Pré-requis à configurer

- `STAGING_URL` et `PRODUCTION_URL` dans les environnements GitHub correspondants ;
- un mécanisme d'accès au serveur ou à l'orchestrateur, stocké dans GitHub Secrets ;
- une image GHCR précédente conservée et accessible ;
- une sauvegarde de base avant migration en production ;
- une règle de reviewers requis sur l'environnement `production`.

## Procédure

1. Identifier `PREVIOUS_IMAGE_DIGEST` dans l'artefact de la release précédente.
2. Redéployer exactement `ghcr.io/<organisation>/<depot>/gestion-api@$PREVIOUS_IMAGE_DIGEST` avec le mécanisme d'infrastructure configuré.
3. Exécuter `scripts/deploy/smoke_test.ps1 -BaseUrl $env:PRODUCTION_URL`.
4. Vérifier `/health`, la version et le commit retournés.
5. Documenter l'incident et conserver l'image fautive pour analyse.

La commande d'orchestration n'est volontairement pas fournie ici : le TP ne définit ni serveur ni plateforme de déploiement. Aucun faux endpoint ni secret ne doit être ajouté au dépôt.
