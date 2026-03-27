from fastapi import FastAPI
from app.api import products, categories, orders
from app.db import database, engine, metadata

metadata.create_all(engine)

app = FastAPI(title="Furni Shop API", version="1.0.0")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/ping")
async def ping():
    return {"ping": "pong!"}