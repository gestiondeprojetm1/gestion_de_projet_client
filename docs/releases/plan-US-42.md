# Plan US-42 — Gestion du stock

1. Déclarer ou modifier le stock d'un produit.
2. Retourner le stock dans `GET /products`.
3. Refuser une commande si le stock est insuffisant avec HTTP 409.
4. Décrémenter le stock dans la même transaction que la commande.
5. Vérifier le comportement concurrent sur PostgreSQL.
6. Publier une image immuable après validation CI.

## Critères de validation

- stock entier supérieur ou égal à zéro ;
- quantité de commande strictement positive ;
- aucune vente ne rend le stock négatif ;
- une commande refusée ne modifie ni le stock ni les commandes ;
- l'image staging et l'image production devront être le même digest lors de D2.2.
