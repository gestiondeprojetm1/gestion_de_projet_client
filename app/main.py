"""API REST : santé, catalogue de produits et commandes."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.config import APP_VERSION, GIT_SHA
from app.database import get_db, init_db
from app.models import Order, Product
from app.schemas import OrderIn, OrderOut, ProductOut


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="API commandes", version=APP_VERSION, lifespan=lifespan)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Indique la version déployée (risque 2 du T1) et l'état de la base."""
    try:
        db.execute(text("SELECT 1"))
        database = "ok"
    except Exception:
        database = "error"
    return {"status": "ok", "version": APP_VERSION, "commit": GIT_SHA, "database": database}


@app.get("/products", response_model=list[ProductOut])
def list_products(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Product).order_by(Product.id).limit(limit).offset(offset)
    return db.scalars(query).all()


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order_in: OrderIn, db: Session = Depends(get_db)):
    # Une quantité invalide (<= 0) est déjà refusée par Pydantic : réponse 422.
    if db.get(Product, order_in.product_id) is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    order = Order(product_id=order_in.product_id, quantity=order_in.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
