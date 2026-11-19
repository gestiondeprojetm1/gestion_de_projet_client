"""Tests de l'API : exécutés à chaque Pull Request (job CI "tests")."""
import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Product


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
    assert set(products[0]) == {"id", "name", "price", "producer", "stock"}
    assert products[0]["stock"] == 10


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
    product = next(p for p in client.get("/products").json() if p["id"] == 1)
    assert product["stock"] == 8


def test_declaration_et_modification_du_stock(client, stock_headers):
    response = client.put("/products/1/stock", json={"stock": 25}, headers=stock_headers)
    assert response.status_code == 200
    assert response.json()["stock"] == 25

    response = client.put("/products/1/stock", json={"stock": 4}, headers=stock_headers)
    assert response.status_code == 200
    assert response.json()["stock"] == 4


def test_commande_stock_insuffisant_et_stock_inchange(client):
    response = client.post("/orders", json={"product_id": 1, "quantity": 11})
    assert response.status_code == 409
    assert response.json()["detail"] == "Stock insuffisant"
    assert client.get("/products").json()[0]["stock"] == 10


def test_stock_produit_inexistant(client, stock_headers):
    response = client.put("/products/9999/stock", json={"stock": 3}, headers=stock_headers)
    assert response.status_code == 404


def test_stock_invalide(client, stock_headers):
    for stock in (-1, 1.5):
        response = client.put("/products/1/stock", json={"stock": stock}, headers=stock_headers)
        assert response.status_code == 422


def test_modification_stock_sans_authentification_refusee(client):
    response = client.put("/products/1/stock", json={"stock": 25})
    assert response.status_code == 401


def test_producteur_ne_peut_pas_modifier_le_produit_d_un_autre(client):
    response = client.put(
        "/products/2/stock",
        json={"stock": 25},
        headers={"Authorization": "Bearer test-rucher-token"},
    )
    assert response.status_code == 403


def test_producteur_autorise_modifie_son_produit(client, stock_headers):
    response = client.put("/products/1/stock", json={"stock": 25}, headers=stock_headers)
    assert response.status_code == 200


def test_la_base_refuse_un_stock_negatif(db_session):
    db_session.add(Product(name="Produit invalide", price=1, producer="Test", stock=-1))
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_health_base_indisponible_retourne_503(broken_client):
    response = broken_client.get("/health")
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["database"] == "error"


def test_commande_produit_inexistant(client):
    response = client.post("/orders", json={"product_id": 9999, "quantity": 1})
    assert response.status_code == 404


def test_commande_quantite_invalide(client):
    for quantity in (0, -3):
        response = client.post("/orders", json={"product_id": 1, "quantity": quantity})
        assert response.status_code == 422
