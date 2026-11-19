"""API REST : santé, catalogue de produits et commandes."""
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from hmac import compare_digest
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session

from app.config import APP_VERSION, GIT_SHA, get_producer_tokens
from app.database import get_db, init_db
from app.models import Order, Product
from app.schemas import OrderIn, OrderOut, ProductOut, StockUpdate


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title="API commandes", version=APP_VERSION, lifespan=lifespan)
bearer_scheme = HTTPBearer(auto_error=False)


def authenticated_producer(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    """Authentifie un producteur avec un jeton stocké côté serveur."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification producteur requise",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        producer_tokens = get_producer_tokens()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentification producteur non configurée",
        ) from exc
    for token, producer in producer_tokens.items():
        if compare_digest(credentials.credentials, token):
            return producer
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton producteur invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Indique la version déployée (risque 2 du T1) et l'état de la base."""
    try:
        db.execute(text("SELECT 1"))
        database = "ok"
    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "version": APP_VERSION,
                "commit": GIT_SHA,
                "database": "error",
                "detail": "Service non prêt : base de données indisponible",
            },
        )
    return {"status": "ok", "version": APP_VERSION, "commit": GIT_SHA, "database": "ok"}


@app.get("/products", response_model=list[ProductOut])
def list_products(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Product).order_by(Product.id).limit(limit).offset(offset)
    return db.scalars(query).all()


@app.put("/products/{product_id}/stock", response_model=ProductOut)
def update_stock(
    product_id: int,
    stock_in: StockUpdate,
    producer: str = Depends(authenticated_producer),
    db: Session = Depends(get_db),
):
    """Déclare le stock disponible d'un produit.

    Le producteur est déduit d'un jeton Bearer configuré côté serveur.
    """
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    if not compare_digest(product.producer, producer):
        raise HTTPException(status_code=403, detail="Accès interdit pour ce producteur")
    product.stock = stock_in.stock
    db.commit()
    db.refresh(product)
    return product


@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(order_in: OrderIn, db: Session = Depends(get_db)):
    # Une quantité invalide (<= 0) est déjà refusée par Pydantic : réponse 422.
    # UPDATE conditionnel : PostgreSQL verrouille la ligne et ne décrémente
    # que si le stock restant est suffisant. Cela rend l'opération atomique.
    result = db.execute(
        update(Product)
        .where(Product.id == order_in.product_id, Product.stock >= order_in.quantity)
        .values(stock=Product.stock - order_in.quantity)
    )
    if result.rowcount == 0:
        db.rollback()
        if db.get(Product, order_in.product_id) is None:
            raise HTTPException(status_code=404, detail="Produit introuvable")
        raise HTTPException(status_code=409, detail="Stock insuffisant")

    order = Order(product_id=order_in.product_id, quantity=order_in.quantity)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
