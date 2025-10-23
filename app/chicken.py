from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List,Literal
from sqlalchemy.orm import Session
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.services.chicken_service import ChickenShopService
from src.models.chicken_setup import (
    ProductCreateRequest,
    ProductResponse,
    ProductListResponse,
    ProductUpdateRequest,
    BuyRequest,
    BuyResponse,
    DeleteResponse
)
from database import get_db





chicken_service = ChickenShopService()
app = FastAPI(title="Chicken Shop Vending Machine")

# products = {
#     "1": {"name": "Whole Chicken", "price_per_kg": 160, "stock_kg": 50},
#     "2": {"name": "Drumsticks", "price_per_kg": 500, "stock_kg": 20},
#     "3": {"name": "Wings", "price_per_kg": 400, "stock_kg": 15},
#     "4": {"name": "Breast", "price_per_kg": 320, "stock_kg": 10},
# }


class BuyRequest(BaseModel):
    product_id: str
    quantity_kg: float
    money_inserted: float

# ✅ Define this BEFORE using it in PUT
class Product(BaseModel):
    name: str
    price_per_kg: float
    stock_kg: float


# ----------------------------
# API Routes
# ----------------------------

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/products")
async def get_products(db: Session = Depends(get_db)):
    return await chicken_service.get_all_products(db)


@app.post("/products", response_model=ProductResponse)
async def create_product(req: ProductCreateRequest, db: Session = Depends(get_db)):
    return await chicken_service.create_product(
        product_name=req.product_name,
        price_per_kg=req.price_per_kg,
        stock_kg=req.stock_kg,
        db=db
    )


@app.get("/products", response_model=List[ProductListResponse])
async def get_products(db: Session = Depends(get_db)):
    return await chicken_service.get_all_products(db)


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    return await chicken_service.get_product_by_id(product_id, db)


@app.put("/products", response_model=ProductResponse)
async def update_product(req: ProductUpdateRequest, db: Session = Depends(get_db)):
    return await chicken_service.update_product(
        product_id=req.product_id,
        product_name=req.product_name,
        price_per_kg=req.price_per_kg,
        stock_kg=req.stock_kg,
        db=db
    )


@app.delete("/products/{product_id}", response_model=DeleteResponse)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    return await chicken_service.delete_product(product_id, db)


@app.post("/buy", response_model=BuyResponse)
async def buy_product(req: BuyRequest, db: Session = Depends(get_db)):
    return await chicken_service.buy_product(
        product_id=req.product_id,
        quantity_kg=req.quantity_kg,
        money_inserted=req.money_inserted,
        db=db
    )