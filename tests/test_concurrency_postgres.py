"""Test de concurrence PostgreSQL, activé avec TEST_POSTGRES_URL."""
import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Order, Product


POSTGRES_URL = os.getenv("TEST_POSTGRES_URL")
pytestmark = pytest.mark.skipif(not POSTGRES_URL, reason="TEST_POSTGRES_URL non configurée")


def test_commandes_concurrentes_ne_vendent_pas_plus_que_le_stock():
    from app.main import create_order
    from app.schemas import OrderIn

    admin_engine = create_engine(POSTGRES_URL, pool_pre_ping=True)
    schema = f"test_stock_{uuid4().hex}"
    with admin_engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA "{schema}"'))
    engine = create_engine(
        POSTGRES_URL,
        pool_pre_ping=True,
        connect_args={"options": f"-csearch_path={schema}"},
    )
    sessions = sessionmaker(bind=engine, autoflush=False)
    try:
        Base.metadata.create_all(bind=engine)
        with sessions() as db:
            product = Product(name="Test concurrence", price=1, producer="Test", stock=1)
            db.add(product)
            db.commit()
            product_id = product.id

        def place_order():
            with sessions() as db:
                try:
                    create_order(OrderIn(product_id=product_id, quantity=1), db)
                    return 201
                except Exception as exc:
                    return getattr(exc, "status_code", None)

        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = list(pool.map(lambda _: place_order(), range(2)))

        with sessions() as db:
            product = db.get(Product, product_id)
            orders = db.query(Order).filter(Order.product_id == product_id).count()
            assert product.stock == 0
            assert orders == 1
        assert sorted(statuses) == [201, 409]
    finally:
        engine.dispose()
        with admin_engine.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin_engine.dispose()
