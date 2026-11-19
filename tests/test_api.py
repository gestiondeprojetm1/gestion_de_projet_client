"""Tests de l'API : exécutés à chaque Pull Request (job CI "tests")."""


def test_health_affiche_version_et_base(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
    assert "version" in body
    assert "commit" in body


def test_liste_des_produits(client):
    response = client.get("/products")
    assert response.status_code == 200
    products = response.json()
    assert len(products) == 3
    assert set(products[0]) == {"id", "name", "price", "producer"}


def test_pagination_des_produits(client):
    response = client.get("/products", params={"limit": 2, "offset": 1})
    assert response.status_code == 200
    assert [p["name"] for p in response.json()] == ["Cidre Fermier", "Beurre Local"]


def test_limit_superieure_a_100_refusee(client):
    assert client.get("/products", params={"limit": 101}).status_code == 422


def test_creation_commande_valide(client):
    response = client.post("/orders", json={"product_id": 1, "quantity": 2})
    assert response.status_code == 201
    body = response.json()
    assert body["product_id"] == 1
    assert body["quantity"] == 2
    assert "id" in body and "created_at" in body


def test_commande_produit_inexistant(client):
    response = client.post("/orders", json={"product_id": 9999, "quantity": 1})
    assert response.status_code == 404


def test_commande_quantite_invalide(client):
    for quantity in (0, -3):
        response = client.post("/orders", json={"product_id": 1, "quantity": quantity})
        assert response.status_code == 422
