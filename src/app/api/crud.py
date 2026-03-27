from app.api.models import ProductSchema, CategorySchema, OrderSchema
from app.db import products, categories, orders, order_items, database


# --- Products ---
async def get_all_products():
    return await database.fetch_all(products.select())

async def get_product(id: int):
    return await database.fetch_one(products.select().where(products.c.id == id))

async def post_product(payload: ProductSchema):
    query = products.insert().values(**payload.dict())
    return await database.execute(query=query)

async def put_product(id: int, payload: ProductSchema):
    query = products.update().where(products.c.id == id).values(**payload.dict())
    return await database.execute(query=query)

async def delete_product(id: int):
    return await database.execute(products.delete().where(products.c.id == id))


# --- Categories ---
async def get_all_categories():
    return await database.fetch_all(categories.select())

async def get_category(id: int):
    return await database.fetch_one(categories.select().where(categories.c.id == id))

async def post_category(payload: CategorySchema):
    query = categories.insert().values(name=payload.name)
    return await database.execute(query=query)

async def delete_category(id: int):
    return await database.execute(categories.delete().where(categories.c.id == id))


# --- Orders ---
async def post_order(customer_name: str, customer_email: str, total_amount, items: list):
    query = orders.insert().values(
        customer_name=customer_name,
        customer_email=customer_email,
        total_amount=total_amount,
        status="pending"
    )
    order_id = await database.execute(query=query)
    for item in items:
        await database.execute(order_items.insert().values(
            order_id=order_id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price=item["unit_price"]
        ))
    return order_id

async def get_order(id: int):
    return await database.fetch_one(orders.select().where(orders.c.id == id))