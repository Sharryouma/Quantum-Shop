from fastapi import APIRouter, HTTPException
from app.api import crud
from app.api.models import OrderSchema, OrderDB

router = APIRouter()


@router.post("/", response_model=OrderDB, status_code=201, summary="Place an order")
async def create_order(payload: OrderSchema):
    total = 0
    enriched_items = []
    for item in payload.items:
        product = await crud.get_product(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        unit_price = float(product["price"])
        total += unit_price * item.quantity
        enriched_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": unit_price
        })
    order_id = await crud.post_order(
        payload.customer_name, payload.customer_email, round(total, 2), enriched_items
    )
    return {
        "id": order_id,
        "customer_name": payload.customer_name,
        "customer_email": payload.customer_email,
        "total_amount": round(total, 2),
        "status": "pending"
    }


@router.get("/{id}/", response_model=OrderDB, summary="Get order by ID")
async def read_order(id: int):
    order = await crud.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order