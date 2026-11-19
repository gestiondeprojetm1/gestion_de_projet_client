"""Schémas Pydantic : validation des entrées et format des réponses."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    producer: str
    stock: int


class StockUpdate(BaseModel):
    stock: int = Field(ge=0, description="Stock entier non négatif")


class OrderIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Quantité strictement positive")


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    created_at: datetime
