import json

from fastapi import FastAPI, Response, status
# from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    description: str = ""
    price: float
    stock: int

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
def get_product(id: int, response: Response):
    product = None
    for p in products:
        if p["id"] == id:
            product = p

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"product with id {id} was not found"}
    return {"product": product}


@app.post("/create")
def create_product(new_product: Product):
    print(new_product.model_dump())
    products.append(new_product.model_dump())
    print(products)
    return {"message": new_product}