from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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
    email: EmailStr
    password: str

class ChangePassword(BaseModel):
    password: str

class SellerResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class SellerLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

