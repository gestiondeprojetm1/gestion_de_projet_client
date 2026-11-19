
## 2. Tableau des étapes du pipeline

Nous avons défini les différentes étapes du pipeline CI/CD, depuis la création d'une branche jusqu'au déploiement en production. Pour chacune, nous précisons son déclencheur, sa durée estimée et son caractère bloquant.

| **Étape** | **Déclencheur** | **Durée estimée** | **Bloquante ?** |
|---|---|---|---|
| Création d'une branche | Début d'une nouvelle fonctionnalité ou correction depuis `main` | Variable | Non |
| Ouverture de la Pull Request | Création d'une PR depuis une branche `feature`, `fix` ou `hotfix` | Moins de 1 min | Non |
| Lint et tests automatisés | Chaque push sur la PR | 1 à 3 min | Oui, en cas d'échec |
| Scan des secrets | Chaque push sur la PR | Moins de 1 min | Oui, si un secret est détecté |
| Build de l'image Docker sans publication | Après les tests et le scan des secrets | 2 à 5 min | Oui, en cas d'échec |
| Relecture du code et approbation humaine 1 | CI réussie et PR prête à être examinée | 5 à 15 min (hors attente) | Oui, sans approbation |
| Fusion dans `main` | CI réussie et PR approuvée | Moins de 1 min | Oui, si les conditions ne sont pas respectées |
| Création du tag SemVer `vX.Y.Z` | Fusion dans `main` | Moins de 1 min | Oui, si le tag ne peut pas être créé |
| Build et publication de l'image sur GHCR | Création du tag SemVer | 2 à 5 min | Oui, en cas d'échec |
| Déploiement en staging et migrations de la base | Image Docker publiée sur GHCR | 2 à 5 min | Oui, en cas d'échec |
| Tests de fumée | Déploiement en staging terminé | 1 à 3 min | Oui, en cas d'échec |
| Approbation humaine 2 | Tests de staging réussis | Variable selon la disponibilité du responsable | Oui, sans approbation |
| Sauvegarde de la base de données | Approbation de la mise en production | 1 à 2 min | Oui, si la sauvegarde échoue |
| Migrations et déploiement en production | Sauvegarde terminée | 2 à 3 min | Oui, en cas d'échec |
| Vérification finale du service | Déploiement en production terminé | 1 à 2 min | Oui, déclenche un rollback si le service ne fonctionne pas |

*Ces durées sont des estimations et devront être vérifiées pendant la réalisation du projet. Les temps d'attente des relecteurs et des responsables ne sont pas inclus.*

**Justification :**

Les contrôles automatisés permettent de détecter les erreurs et les éventuels secrets exposés avant la fusion dans `main`. La première approbation humaine garantit qu'un autre développeur valide les modifications, avec une relecture par un développeur senior via CODEOWNERS lorsque l'auteur est un alternant.

Après la fusion, l'image Docker est construite et publiée sur GHCR, puis déployée en staging afin de vérifier le fonctionnement de l'application. Une deuxième approbation humaine, réalisée dans l'environnement GitHub `production`, est nécessaire avant le déploiement en production. Enfin, la sauvegarde de la base de données et la vérification finale permettent de limiter les risques liés au déploiement.
