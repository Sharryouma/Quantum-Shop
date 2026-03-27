from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class CategoryDB(CategorySchema):
    id: int


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Decimal = Field(..., gt=0)
    image_url: Optional[str] = None
    stock: int = Field(0, ge=0)
    category_id: Optional[int] = None

class ProductDB(ProductSchema):
    id: int


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderSchema(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    customer_email: str = Field(..., max_length=100)
    items: List[OrderItemSchema]

class OrderDB(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    total_amount: Decimal
    status: str