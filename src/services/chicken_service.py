from fastapi import HTTPException
from sqlalchemy.orm import Session
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from models import Product, EnumStatus, Transaction, TransactionStatus


class ChickenShopService:
    async def create_product(self, product_name: str, price_per_kg: float, stock_kg: float, db: Session):
        """Create a new product"""
        product = Product(
            PRODUCT_NAME=product_name,
            PRICE_PER_KG=price_per_kg,
            STOCK_KG=stock_kg,
            STATUS=EnumStatus.ACTIVE
        )
        db.add(product)
        db.commit()
        db.refresh(product)

        return {
            "product_id": product.PRODUCT_ID,
            "name": product.PRODUCT_NAME,
            "price_per_kg": float(product.PRICE_PER_KG),
            "stock_kg": float(product.STOCK_KG),
            "status": product.STATUS.value
        }

    async def get_all_products(self, db: Session):
        """Get all active products from the database"""
        products = db.query(Product).filter(Product.STATUS == EnumStatus.ACTIVE).order_by(Product.PRODUCT_ID).all()
        return [
            {
                "product_id": p.PRODUCT_ID,
                "name": p.PRODUCT_NAME,
                "price_per_kg": float(p.PRICE_PER_KG),
                "stock_kg": float(p.STOCK_KG)
            }
            for p in products
        ]

    async def get_product_by_id(self, product_id: int, db: Session):
        """Get a specific product by ID"""
        product = db.query(Product).filter(
            Product.PRODUCT_ID == product_id,
            Product.STATUS == EnumStatus.ACTIVE
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "product_id": product.PRODUCT_ID,
            "name": product.PRODUCT_NAME,
            "price_per_kg": float(product.PRICE_PER_KG),
            "stock_kg": float(product.STOCK_KG),
            "created_at": product.CREATED_AT,
            "updated_at": product.UPDATED_AT,
            "status": product.STATUS.value
        }

    async def update_product(self, product_id: int, product_name: str = None, price_per_kg: float = None, stock_kg: float = None, db: Session = None):
        """Update an existing product"""
        product = db.query(Product).filter(
            Product.PRODUCT_ID == product_id,
            Product.STATUS == EnumStatus.ACTIVE
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Update only the fields that are provided
        if product_name is not None:
            product.PRODUCT_NAME = product_name
        if price_per_kg is not None:
            product.PRICE_PER_KG = price_per_kg
        if stock_kg is not None:
            product.STOCK_KG = stock_kg

        db.commit()
        db.refresh(product)

        return {
            "product_id": product.PRODUCT_ID,
            "name": product.PRODUCT_NAME,
            "price_per_kg": float(product.PRICE_PER_KG),
            "stock_kg": float(product.STOCK_KG),
            "status": product.STATUS.value
        }

    async def delete_product(self, product_id: int, db: Session):
        """Soft delete a product by setting status to INACTIVE"""
        product = db.query(Product).filter(
            Product.PRODUCT_ID == product_id,
            Product.STATUS == EnumStatus.ACTIVE
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.STATUS = EnumStatus.INACTIVE
        db.commit()

        return {
            "message": f"Product '{product.PRODUCT_NAME}' deleted successfully",
            "product_id": product_id
        }

    async def buy_product(self, product_id: int, quantity_kg: float, money_inserted: float, db: Session):
        """Process a product purchase"""
        # Find the product
        product = db.query(Product).filter(
            Product.PRODUCT_ID == product_id,
            Product.STATUS == EnumStatus.ACTIVE
        ).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        stock_kg = float(product.STOCK_KG)
        price_per_kg = float(product.PRICE_PER_KG)

        # Validate stock availability
        if quantity_kg > stock_kg:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock. Only {stock_kg} kg available"
            )

        # Calculate total cost
        total_cost = price_per_kg * quantity_kg

        # Validate payment
        if money_inserted < total_cost:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough money. Total cost is ₹{total_cost}"
            )

        # Process the transaction
        change = money_inserted - total_cost

        # Update stock
        product.STOCK_KG = stock_kg - quantity_kg

        # Create transaction record
        transaction = Transaction(
            PRODUCT_ID=product_id,
            QUANTITY_KG=quantity_kg,
            PRICE_AT_PURCHASE=price_per_kg,
            TOTAL_COST=total_cost,
            MONEY_INSERTED=money_inserted,
            CHANGE_RETURNED=change,
            STATUS=TransactionStatus.SUCCESS
        )

        db.add(transaction)
        db.commit()
        db.refresh(product)
        db.refresh(transaction)

        return {
            "transaction_id": transaction.TRANSACTION_ID,
            "message": f"Dispensed {quantity_kg} kg of {product.PRODUCT_NAME}",
            "total_cost": total_cost,
            "change": change,
            "remaining_stock": float(product.STOCK_KG)
        }
