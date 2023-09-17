from pydantic import BaseModel, Field
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(max_length=100)
    price: float
    stock: int
    description: str


class ProductInput(ProductBase):
    pass


class ProductOutput(ProductBase):
    created_at: datetime
    updated_at: datetime
