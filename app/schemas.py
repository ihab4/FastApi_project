from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int


class CreateProduct(ProductBase):
    pass

class UpdateProduct(BaseModel):
    price: float
    stock: int

class ProductResponse(ProductBase):
    created_at: datetime
    id: int

    class Config:
        from_attributes = True



class CreateSeller(BaseModel):
    email: str
    password: str

class ChangePassword(BaseModel):
    password: str

class SellerResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
