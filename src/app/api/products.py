from typing import List
from fastapi import APIRouter, HTTPException, Path
from app.api import crud
from app.api.models import ProductSchema, ProductDB

router = APIRouter()


@router.get("/", response_model=List[ProductDB], summary="List all products")
async def read_all_products():
    return await crud.get_all_products()


@router.get("/{id}/", response_model=ProductDB, summary="Get a product by ID")
async def read_product(id: int = Path(..., gt=0)):
    product = await crud.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductDB, status_code=201, summary="Create a product")
async def create_product(payload: ProductSchema):
    product_id = await crud.post_product(payload)
    return {"id": product_id, **payload.dict()}


@router.put("/{id}/", response_model=ProductDB, summary="Update a product")
async def update_product(payload: ProductSchema, id: int = Path(..., gt=0)):
    product = await crud.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await crud.put_product(id, payload)
    return {"id": id, **payload.dict()}


@router.delete("/{id}/", response_model=ProductDB, summary="Delete a product")
async def delete_product(id: int = Path(..., gt=0)):
    product = await crud.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await crud.delete_product(id)
    return product