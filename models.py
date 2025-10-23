import enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.types import NUMERIC, VARCHAR

from database import Base


class EnumStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class TransactionStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    REFUNDED = "REFUNDED"


class Product(Base):
    __tablename__ = "products"

    PRODUCT_ID = Column(Integer, primary_key=True, autoincrement=True)
    PRODUCT_NAME = Column(VARCHAR(100), nullable=False)
    PRICE_PER_KG = Column(NUMERIC(precision=10, scale=2), nullable=False)
    STOCK_KG = Column(NUMERIC(precision=10, scale=2), default=0, nullable=False)
    CREATED_AT = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    UPDATED_AT = Column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    STATUS = Column(Enum(EnumStatus), default=EnumStatus.ACTIVE, nullable=False)

    transactions = relationship("Transaction", back_populates="product")


class Transaction(Base):
    __tablename__ = "transactions"

    TRANSACTION_ID = Column(Integer, primary_key=True, autoincrement=True)
    PRODUCT_ID = Column(Integer, ForeignKey("products.PRODUCT_ID"), nullable=False)
    QUANTITY_KG = Column(NUMERIC(precision=10, scale=2), nullable=False)
    PRICE_AT_PURCHASE = Column(NUMERIC(precision=10, scale=2), nullable=False)
    TOTAL_COST = Column(NUMERIC(precision=10, scale=2), nullable=False)
    MONEY_INSERTED = Column(NUMERIC(precision=10, scale=2), nullable=False)
    CHANGE_RETURNED = Column(NUMERIC(precision=10, scale=2), nullable=False)
    TRANSACTION_DATETIME = Column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False
    )
    STATUS = Column(Enum(TransactionStatus), default=TransactionStatus.SUCCESS, nullable=False)

    product = relationship("Product", back_populates="transactions")
