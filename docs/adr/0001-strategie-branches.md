# T2 — Stratégie de branches

## 1. Choix de la stratégie

Nous avons choisi **GitHub Flow** pour organiser le travail de notre équipe composée de 6 développeurs, dont 2 alternants.

Cette stratégie permet à chaque développeur de travailler sur sa propre branche sans modifier directement la branche principale `main`.

Elle facilite la collaboration, la relecture du code et la validation des modifications avant leur intégration dans la branche principale et leur déploiement.

Ce fonctionnement permet également de limiter les risques liés à l'intégration de code non vérifié dans le projet.

## 2. Organisation des branches

| Branche | Utilisation | Responsable |
|---|---|---|
| `main` | Contient le code validé et stable | Toute l'équipe, après validation |
| `feature/nom-fonctionnalite` | Développement d'une nouvelle fonctionnalité | Développeur responsable |
| `fix/nom-correction` | Correction d'un bug non urgent | Développeur responsable |
| `hotfix/nom-probleme` | Correction d'un problème urgent en production | Développeur désigné |

La branche `main` est protégée : aucun développeur ne peut y intégrer directement ses modifications sans passer par une Pull Request.

## 3. Fonctionnement de la stratégie

Le travail de l'équipe suit les étapes suivantes :

1. Chaque développeur crée une branche à partir de la dernière version de `main`.
2. Il développe sa fonctionnalité ou effectue sa correction sur cette branche.
3. Il réalise des tests pour vérifier que ses modifications fonctionnent correctement.
4. Il ouvre une **Pull Request (PR)** sur GitHub afin de proposer l'intégration de son travail dans `main`.
5. Les tests automatisés sont exécutés par le pipeline CI/CD.
6. Un autre développeur relit le code et donne son approbation. Au moins une approbation est obligatoire avant la fusion.
7. Si les tests et la relecture sont validés, la Pull Request peut être fusionnée dans `main`.
8. La nouvelle version est ensuite déployée en staging afin d'être vérifiée.
9. Le déploiement en production nécessite une approbation humaine.

Les alternants suivent le même processus que les autres développeurs, avec un accompagnement lors des revues de code. Les modifications sensibles qu'ils proposent doivent notamment être relues par un développeur senior, conformément aux règles définies dans le fichier `CODEOWNERS`.

## 4. Gestion des corrections urgentes

Si un problème important apparaît en production, une branche `hotfix` est créée à partir de la version stable afin de corriger rapidement le problème.

Le correctif doit suivre les étapes suivantes :

1. Création d'une branche `hotfix` à partir de `main`.
2. Correction du problème par le développeur désigné.
3. Exécution des tests automatisés.
4. Ouverture d'une Pull Request et relecture du correctif.
5. Vérification du correctif en staging.
6. Fusion dans `main` après validation.
7. Déploiement en production après approbation d'un responsable.

Après la fusion, les autres développeurs récupèrent la dernière version de `main` dans leurs branches afin d'intégrer le correctif à leur travail en cours.

## 5. Comment savoir si cette stratégie ne fonctionne plus ?

Nous pouvons considérer que notre stratégie n'est plus adaptée si plusieurs problèmes apparaissent régulièrement :

- Les Pull Requests restent trop longtemps en attente, par exemple plus de deux jours.
- Les conflits entre les branches deviennent trop fréquents.
- Des erreurs importantes arrivent régulièrement en production malgré les validations.
- Les développeurs rencontrent des difficultés à intégrer leur travail.
- Les délais de validation ralentissent fortement le développement de l'équipe.

Dans ce cas, nous devrons revoir notre organisation et améliorer les règles de collaboration afin de conserver un processus de développement efficace.

## 6. Justification du choix et lien avec l'analyse des risques (T1)

Le choix de GitHub Flow répond directement à plusieurs risques identifiés dans notre analyse des risques (T1).

- **Déployer une version non testée :** les tests automatisés, le passage en staging et l'approbation humaine avant la production permettent de limiter ce risque.
- **Code fusionné sans relecture :** les Pull Requests obligatoires, les approbations et la protection de `main` empêchent l'intégration directe de modifications non vérifiées.
- **Migration incorrecte de la base de données :** les tests automatisés et la vérification en staging permettent de détecter certains problèmes avant la mise en production.
- **Accompagnement des alternants :** les revues de code permettent aux développeurs plus expérimentés de vérifier les modifications et d'accompagner les alternants.

Les autres risques identifiés dans le T1, notamment la fuite de secrets, l'identification des versions et le rollback, seront traités par les mesures de sécurité et de déploiement prévues dans le projet.

Notre objectif est de permettre aux six développeurs de travailler efficacement en parallèle, tout en garantissant la qualité du code, la traçabilité des modifications et la stabilité de l'application.