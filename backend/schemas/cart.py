from decimal import Decimal
from pydantic import BaseModel, Field, computed_field

from schemas.product import ProductResponse

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, default=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)

class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int

    model_config = {'from_attributes': True}

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity

class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]

    model_config = {'from_attributes': True}

    @computed_field
    @property
    def total(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal('0'))