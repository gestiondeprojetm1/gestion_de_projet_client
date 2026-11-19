"""Insère 1 200 produits de démonstration.

Idempotent : si la table products contient déjà des produits, rien n'est ajouté.
Lancement : docker compose run --rm api python scripts/seed.py
"""
import random
from decimal import Decimal

from sqlalchemy import func, select

from app.database import SessionLocal, init_db
from app.models import Product

NB_PRODUCTS = 1200

ADJECTIVES = ["Bio", "Fermier", "Artisanal", "Local", "Frais", "Tradition", "Premium", "de Saison"]
ITEMS = [
    "Miel", "Fromage de chèvre", "Confiture", "Jus de pomme", "Pain complet",
    "Huile d'olive", "Lentilles", "Yaourt", "Saucisson", "Farine", "Oeufs",
    "Tomates", "Pommes de terre", "Vin rouge", "Cidre", "Beurre", "Noix",
]
PRODUCER_PREFIXES = ["Ferme", "Domaine", "Maison", "Les Jardins", "Moulin", "Rucher"]
PRODUCER_NAMES = ["du Lac", "des Collines", "Martin", "Dubois", "du Vallon", "Saint-Jean", "Bernard", "des Prés"]


def generate_products(count: int) -> list[Product]:
    rng = random.Random(42)  # graine fixe : mêmes données à chaque exécution
    products = []
    for i in range(1, count + 1):
        name = f"{rng.choice(ITEMS)} {rng.choice(ADJECTIVES)} n°{i}"
        producer = f"{rng.choice(PRODUCER_PREFIXES)} {rng.choice(PRODUCER_NAMES)}"
        price = Decimal(str(round(rng.uniform(0.99, 49.99), 2)))
        products.append(Product(name=name, price=price, producer=producer))
    return products


def main() -> None:
    init_db()
    with SessionLocal() as db:
        existing = db.scalar(select(func.count()).select_from(Product))
        if existing:
            print(f"{existing} produits déjà présents : aucune insertion.")
            return
        db.add_all(generate_products(NB_PRODUCTS))
        db.commit()
        print(f"{NB_PRODUCTS} produits insérés.")


if __name__ == "__main__":
    main()
