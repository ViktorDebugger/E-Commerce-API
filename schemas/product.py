from decimal import Decimal
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0, default=0)

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int

    model_config = {'from_attributes': True}