from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    price: Decimal
    quantity: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    status: str
    total: Decimal
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = {"from_attributes": True}


class CheckoutResponse(BaseModel):
    order: OrderResponse
    client_secret: str