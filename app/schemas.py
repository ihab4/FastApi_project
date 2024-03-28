from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int


class CreateProduct(ProductBase):
    pass

class ProductResponse(BaseModel):
    name: str
    description: str
    price: float
    # stock: int
    created_at: datetime

    class Config:
        from_attributes = True



class CreateSeller(BaseModel):
    email: str
    password: str


class SellerResponse(BaseModel):
    id: int
    email: str
    # created_at: datetime

    class Config:
        from_attributes = True