# T1 — Analyse des risques

## 1. Contexte et identification des risques

L'objectif de cette analyse est d'identifier les principaux risques liés au développement, à la sécurité et au déploiement de notre application.

Notre équipe est composée de 6 développeurs, dont 2 alternants. La société travaille avec plusieurs clients simultanément. Il est donc essentiel de mettre en place une organisation fiable, permettant de valider chaque version de l'application avant son déploiement en production.

## 2. Échelle de notation

Pour faciliter la comparaison des risques, nous attribuons une note de 1 à 5 à chaque dimension : la gravité et l'effort.

### 2.1 Échelle de gravité

| **Note** | **Niveau** |
|:---:|---|
| 1 | Très faible |
| 2 | Faible |
| 3 | Moyenne |
| 4 | Élevée |
| 5 | Critique |

### 2.2 Échelle d'effort

| **Note** | **Niveau** |
|:---:|---|
| 1 | Très faible |
| 2 | Faible |
| 3 | Moyen |
| 4 | Élevé |
| 5 | Très élevé |

## 3. Identification des risques

| **#** | **Risque** | **Scénario de défaillance** | **Gravité** | **Mesure préventive** | **Effort** |
|:---:|---|---|:---:|---|:---:|
| 1 | **Déployer une version non testée** | Un push sur `main` part directement en production sans tests, comme lors de l'incident d'août, et les commandes sont bloquées pendant 14 h. | 5 | Tests obligatoires dans la CI, déploiement d'abord en staging, puis **approbation manuelle** avant la production. | 3 |
| 2 | **Ne pas savoir quelle version tourne** | Une panne survient en production mais personne ne sait ce qui est déployé, donc impossible de revenir en arrière rapidement. | 4 | Tags SemVer (`v1.2.0`), image taguée par version et SHA (jamais `latest`), version affichée dans `/health`. | 2 |
| 3 | **Fuite de secrets et de mots de passe** | Le `.env` versionné est visible sur le dépôt public, et quelqu'un récupère le mot de passe de la base. | 5 | Secrets uniquement dans GitHub Secrets, `.env` dans `.gitignore`, scan de secrets dans la CI, rotation immédiate en cas de fuite. | 2 |
| 4 | **Code mergé sans relecture** | Un alternant ou le freelance pousse directement sur `main`, et un bug part sans que personne ne l'ait vu. | 4 | Protection de `main`, PR obligatoire avec 1 approbation, CODEOWNERS pour imposer un senior sur les PR des alternants. | 2 |
| 5 | **Migration incorrecte de la base** | Une modification de la base de données empêche l'API de fonctionner correctement. | 4 | Migrations automatisées et contrôlées, testées en staging avant leur application en production. | 3 |
| 6 | **Rollback impossible ou trop lent** | La nouvelle version plante et il faut tout reconstruire pour revenir en arrière, ce qui prend des heures. | 5 | Garder les images précédentes sur GHCR et redéployer la version précédente en une commande (objectif : moins de 5 min). | 3 |

## 4. Positionnement des risques : Gravité × Effort

### 4.1 Méthode de calcul

La gravité mesure les conséquences possibles d'un risque sur l'activité de l'entreprise.

L'effort représente la difficulté de mise en place des mesures préventives nécessaires pour traiter ce risque.

Les deux dimensions sont notées de 1 à 5.

Le score est calculé selon la formule suivante :

**Score = Gravité × Effort**

### 4.2 Tableau de positionnement

| **#** | **Risque** | **Gravité** | **Effort** | **Score** |
|:---:|---|:---:|:---:|:---:|
| 1 | Déployer une version non testée | 5 | 3 | **15** |
| 2 | Ne pas savoir quelle version tourne | 4 | 2 | **8** |
| 3 | Fuite de secrets et de mots de passe | 5 | 2 | **10** |
| 4 | Code mergé sans relecture | 4 | 2 | **8** |
| 5 | Migration incorrecte de la base | 4 | 3 | **12** |
| 6 | Rollback impossible ou trop lent | 5 | 3 | **15** |

### 4.3 Justification du positionnement

**Risque 1 — Déployer une version non testée (5 × 3 = 15)**

La gravité est critique, car une version défectueuse peut bloquer les commandes et provoquer une interruption importante du service, comme lors de l'incident d'août. L'effort est moyen, car il faut mettre en place des tests automatisés, un environnement de staging et une approbation manuelle avant la production.

**Risque 2 — Ne pas savoir quelle version tourne (4 × 2 = 8)**

La gravité est élevée, car l'absence d'identification de la version complique le diagnostic et le retour à une version stable. L'effort est faible, car l'utilisation de tags Git, de versions SemVer et de tags Docker permet de résoudre ce problème assez simplement.

**Risque 3 — Fuite de secrets et de mots de passe (5 × 2 = 10)**

La gravité est critique, car une fuite de mots de passe peut permettre un accès non autorisé à la base de données. L'effort est faible, car GitHub Secrets, `.gitignore` et les outils de détection de secrets sont relativement simples à mettre en place.

**Risque 4 — Code mergé sans relecture (4 × 2 = 8)**

La gravité est élevée, car une erreur non détectée peut arriver en production et provoquer un dysfonctionnement. L'effort est faible, car la protection de la branche principale, les Pull Requests et les règles d'approbation peuvent être configurées directement sur GitHub.

**Risque 5 — Migration incorrecte de la base (4 × 3 = 12)**

La gravité est élevée, car une mauvaise migration peut rendre certaines fonctionnalités inutilisables et empêcher l'enregistrement des commandes. L'effort est moyen, car il faut organiser les migrations, les tester sur une base de staging et prévoir des sauvegardes.

**Risque 6 — Rollback impossible ou trop lent (5 × 3 = 15)**

La gravité est critique, car une panne peut durer plusieurs heures si l'équipe ne parvient pas à restaurer rapidement la version précédente. L'effort est moyen, car il faut conserver les anciennes images Docker, automatiser le redéploiement et tester régulièrement la procédure de retour arrière.

### 4.4 Conclusion et priorisation

Les risques 1 et 6 sont prioritaires, avec un score de 15. Ils concernent directement la disponibilité de l'application et la capacité de l'équipe à réagir rapidement en cas d'incident.

Le risque 5 vient ensuite avec un score de 12, car les migrations de base de données peuvent provoquer des dysfonctionnements importants.

Le risque 3 est également prioritaire malgré un effort de traitement relativement faible, en raison de ses conséquences potentielles sur la sécurité des données.

Enfin, les risques 2 et 4 doivent être traités dès la mise en place du dépôt grâce aux conventions Git et aux protections GitHub.

Cette analyse permet de concentrer les efforts de l'équipe sur les problèmes qui peuvent avoir les conséquences les plus importantes pour l'entreprise.