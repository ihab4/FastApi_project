from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, text
from datetime import datetime
import time

from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Seller(Base):
    __tablename__ = "seller"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
