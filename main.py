import json

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float

with open("data/products.json") as f:
    products = json.load(f)
    f.close()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/products")
def get_products():
    return {"data": products}

@app.get("/product/{id}")
def get_product(id: int):
    for p in products:
        if p["id"] == id:
            product = p
    print(product)
    return {"product": product}


@app.post("/create")
def create_product(new_product: Product):
    # products.append(new_product)
    print(new_product)
    return {"message": new_product}