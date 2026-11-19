# T3 — Règles de gestion et de contribution

## 1. Relecture du code (Pull Requests)

Chaque modification du projet doit passer par une Pull Request (PR) avant d'être intégrée dans la branche principale `main`.

Nous avons décidé qu'une Pull Request doit être approuvée par **au moins un autre développeur** avant sa fusion.

Les règles suivantes doivent être respectées :

- Les modifications directes sur `main` sont interdites.
- Chaque développeur doit travailler sur une branche dédiée.
- Les tests automatisés doivent réussir avant la fusion.
- Une relecture du code est obligatoire avant toute intégration.
- Si le relecteur habituel est absent, un autre développeur compétent peut effectuer la relecture.
- Si personne n'est disponible, la Pull Request reste en attente et ne peut pas être fusionnée.

Pour les modifications sensibles proposées par les deux alternants, une relecture par un développeur senior sera exigée. Le fichier `CODEOWNERS` permettra de définir les responsables de la relecture de certaines parties du projet.

Ces règles permettent de limiter les erreurs, de garantir la qualité du code et d'accompagner les alternants dans leur travail.

## 2. Conventions de nommage

Pour faciliter l'organisation du travail et la compréhension de l'historique Git, nous avons choisi des conventions de nommage communes à toute l'équipe.

### 2.1. Nommage des branches

| Type de branche | Exemple |
|---|---|
| Nouvelle fonctionnalité | `feature/gestion-stock` |
| Correction d'un bug | `fix/erreur-commande` |
| Correction urgente | `hotfix/probleme-production` |

Ces conventions correspondent à la stratégie GitHub Flow définie dans le T2.

### 2.2. Messages de commit

Nous utilisons également des préfixes pour identifier rapidement le type de modification apportée.

Exemples :

```text
feat: ajout de la gestion du stock
fix: correction du calcul des commandes
test: ajout des tests de l'API
docs: mise à jour de la documentation
```

Ces conventions permettent de comprendre facilement les modifications et de mieux suivre l'historique du projet.

## 3. Définition of Done (tâche terminée)

Une tâche est considérée comme terminée lorsque les conditions suivantes sont respectées :

- Le code est développé et fonctionne correctement.
- Les tests automatisés réussissent.
- La Pull Request a été relue et approuvée par au moins un autre développeur.
- Les éventuels problèmes détectés lors de la relecture ont été corrigés.
- Le code a été fusionné dans `main`.
- La documentation est mise à jour si nécessaire.

Pour les modifications concernant la base de données, les migrations doivent également être testées et vérifiées en staging avant leur mise en production. Une sauvegarde de la base doit être prévue avant une migration en production.

Le respect de ces conditions permet de limiter l'intégration de code incorrect et de réduire les risques identifiés dans le T1.

## 4. Gestion des versions

Nous avons choisi d'utiliser le système de versionnement **Semantic Versioning (SemVer)**, avec des numéros de version comme `v1.0.0`, `v1.1.0` ou `v1.1.1`.

Chaque version mise en production sera associée à un tag Git et à une image Docker identifiée par son numéro de version et l'identifiant SHA du commit correspondant.

Exemple :

```text
v1.2.0
v1.2.0-a1b2c3d
```

Nous éviterons d'utiliser le tag `latest` comme référence pour les déploiements afin de toujours savoir précisément quelle version est utilisée.

La version actuellement déployée sera également affichée dans les informations retournées par la route `/health`.

Nous conserverons les images Docker des versions précédentes afin de pouvoir redéployer rapidement une version stable en cas de problème.

En cas d'incident après un déploiement, notre objectif est de réaliser un rollback en moins de **5 minutes**, conformément à l'analyse des risques du T1.

Cette organisation permet d'identifier précisément la version utilisée en production, de faciliter le diagnostic et de revenir rapidement à une version fonctionnelle.

## 5. Gestion des secrets

Les mots de passe, les clés d'API et les identifiants de la base de données ne doivent jamais être enregistrés dans le dépôt GitHub.

Pour protéger les informations sensibles, nous appliquerons les règles suivantes :

- Les secrets nécessaires aux workflows seront stockés dans GitHub Secrets.
- Les environnements GitHub seront utilisés pour gérer les informations nécessaires aux différents déploiements, notamment staging et production.
- Le fichier `.env`, contenant les variables sensibles utilisées localement, sera ajouté au fichier `.gitignore`.
- Les secrets ne devront jamais être écrits directement dans le code source ou dans les fichiers de configuration versionnés.
- Un outil de détection des secrets sera intégré au pipeline CI afin de repérer d'éventuelles informations sensibles dans le code.
- L'accès aux secrets sera limité aux personnes et aux workflows qui en ont réellement besoin.

En cas de fuite, le secret concerné devra être immédiatement révoqué ou remplacé, et les accès devront être vérifiés.

Ces mesures permettent de réduire les risques de fuite de mots de passe et d'accès non autorisés identifiés dans le T1.

## 6. Gestion du développeur freelance

Le développeur freelance doit respecter les mêmes règles de contribution que les autres membres de l'équipe.

Il doit notamment :

- Travailler sur une branche dédiée.
- Respecter les conventions de nommage.
- Ouvrir une Pull Request pour proposer ses modifications.
- Effectuer les tests nécessaires.
- Obtenir une approbation avant la fusion dans `main`.

Nous lui accordons uniquement les permissions nécessaires à son travail, sans accès direct aux secrets de production.

Même si le freelance souhaite travailler rapidement, les règles de sécurité, de relecture et de validation restent obligatoires.

## 7. Application des règles sur GitHub

Les règles définies précédemment seront appliquées à travers les paramètres du dépôt GitHub et l'organisation de l'équipe.

| Règle | Application |
|---|---|
| Interdire les modifications directes sur `main` | Protection de branche GitHub |
| Exiger une Pull Request | Configuration des règles de branche |
| Exiger au moins une approbation | Configuration des règles de branche |
| Imposer la relecture des modifications sensibles | Fichier `CODEOWNERS` |
| Exiger la réussite des tests | Vérifications obligatoires GitHub Actions |
| Détecter les secrets dans le code | Outil de détection intégré au pipeline CI |
| Stocker les secrets | GitHub Secrets et Environments |
| Respecter les noms des branches et des commits | Discipline de l'équipe |
| Accompagner les alternants | Organisation de l'équipe et relecture par un senior |
| Choisir un relecteur remplaçant | Organisation de l'équipe |
| Respecter les règles par le freelance | Permissions GitHub et discipline de l'équipe |
| Identifier les versions déployées | Tags Git et images Docker versionnées |
| Conserver les versions précédentes | Gestion des images Docker pour le rollback |

Ces configurations seront mises en place lors de la partie pratique sur GitHub.

Des captures d'écran des paramètres et des règles configurées seront ajoutées dans le dossier `docs/config/` afin de justifier leur mise en place.

## 8. Lien avec l'analyse des risques (T1) et la stratégie de branches (T2)

Les règles de gestion définies dans ce document complètent les choix réalisés dans les deux documents précédents.

Elles répondent directement aux risques identifiés dans le T1 :

- **Déployer une version non testée :** les tests automatisés, la vérification en staging et l'approbation humaine avant la production limitent ce risque.
- **Ne pas savoir quelle version tourne :** les tags Git, les identifiants SHA et les images Docker versionnées permettent d'identifier précisément chaque version.
- **Fuite de secrets :** GitHub Secrets, le fichier `.gitignore` et la détection des secrets dans le pipeline CI protègent les informations sensibles.
- **Code fusionné sans relecture :** les Pull Requests obligatoires, les approbations et le fichier `CODEOWNERS` permettent de contrôler les modifications.
- **Migration incorrecte de la base de données :** les tests et les vérifications en staging, ainsi que les sauvegardes, limitent les risques liés aux migrations.
- **Rollback impossible ou trop lent :** la conservation des images Docker précédentes permet de redéployer une version stable avec un objectif de retour en moins de 5 minutes.

Ces règles mettent en application la stratégie GitHub Flow définie dans le T2.

Notre objectif est de permettre aux six développeurs de travailler efficacement en parallèle, tout en garantissant la qualité du code, la sécurité du dépôt et la stabilité de l'application.