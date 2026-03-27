from typing import List
from fastapi import APIRouter, HTTPException, Path
from app.api import crud
from app.api.models import CategorySchema, CategoryDB

router = APIRouter()


@router.get("/", response_model=List[CategoryDB], summary="List all categories")
async def read_all_categories():
    return await crud.get_all_categories()


@router.post("/", response_model=CategoryDB, status_code=201, summary="Create a category")
async def create_category(payload: CategorySchema):
    cat_id = await crud.post_category(payload)
    return {"id": cat_id, "name": payload.name}


@router.delete("/{id}/", response_model=CategoryDB, summary="Delete a category")
async def delete_category(id: int = Path(..., gt=0)):
    cat = await crud.get_category(id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    await crud.delete_category(id)
    return cat