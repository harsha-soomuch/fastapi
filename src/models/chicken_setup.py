from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreateRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100)
    price_per_kg: float = Field(..., gt=0)
    stock_kg: float = Field(..., ge=0)


class ProductResponse(BaseModel):
    product_id: int
    name: str
    price_per_kg: float
    stock_kg: float
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductListResponse(BaseModel):
    product_id: int
    name: str
    price_per_kg: float
    stock_kg: float


class BuyRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity_kg: float = Field(..., gt=0)
    money_inserted: float = Field(..., ge=0)


class BuyResponse(BaseModel):
    transaction_id: int
    message: str
    total_cost: float
    change: float
    remaining_stock: float


class DeleteResponse(BaseModel):
    message: str
    product_id: int


class ProductUpdateRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    product_name: Optional[str] = Field(None, min_length=1, max_length=100)
    price_per_kg: Optional[float] = Field(None, gt=0)
    stock_kg: Optional[float] = Field(None, ge=0)
