from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Chicken Shop Vending Machine")

# Initial stock
products = {
    "1": {"name": "Whole Chicken", "price_per_kg": 250, "stock_kg": 50},
    "2": {"name": "Drumsticks", "price_per_kg": 300, "stock_kg": 20},
    "3": {"name": "Wings", "price_per_kg": 280, "stock_kg": 15},
    "4": {"name": "Breast", "price_per_kg": 320, "stock_kg": 10},
}

# Request model for buying
class BuyRequest(BaseModel):
    product_id: str
    quantity_kg: float
    money_inserted: float

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Get available products
@app.get("/products")
async def get_products():
    return products

# Buy product endpoint
@app.post("/buy")
async def buy_product(req: BuyRequest):
    if req.product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[req.product_id]

    if req.quantity_kg > product["stock_kg"]:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Only {product['stock_kg']} kg available"
        )

    total_cost = product["price_per_kg"] * req.quantity_kg

    if req.money_inserted < total_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough money. Total cost is ₹{total_cost}"
        )

    change = req.money_inserted - total_cost
    product["stock_kg"] -= req.quantity_kg

    return {
        "message": f"Dispensed {req.quantity_kg} kg of {product['name']}",
        "total_cost": total_cost,
        "change": change,
        "remaining_stock": product["stock_kg"]
    }
