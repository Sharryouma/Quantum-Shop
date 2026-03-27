import os
from sqlalchemy import (
    Column, DateTime, Integer, Numeric,
    MetaData, String, Table, ForeignKey, create_engine
)
from sqlalchemy.sql import func
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

categories = Table(
    "categories", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False, unique=True),
)

products = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("description", String(500)),
    Column("price", Numeric(10, 2), nullable=False),
    Column("image_url", String(300)),
    Column("stock", Integer, default=0),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=True),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

orders = Table(
    "orders", metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String(100), nullable=False),
    Column("customer_email", String(100), nullable=False),
    Column("total_amount", Numeric(10, 2), nullable=False),
    Column("status", String(30), default="pending"),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

order_items = Table(
    "order_items", metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", Integer, ForeignKey("orders.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Numeric(10, 2), nullable=False),
)

database = Database(DATABASE_URL)