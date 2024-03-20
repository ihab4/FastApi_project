import json

from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

from os import getenv
from dotenv import load_dotenv
from time import sleep


load_dotenv()

db_name, username, password, host = getenv("db_name"), getenv("username"), getenv("password"), getenv("host")
while True:
    try:
        conn = psycopg2.connect(dbname=db_name, user=username, password=password,
                                host=host, port="5432", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connection was succesfull.")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        sleep(2)

app = FastAPI()



class Product(BaseModel):
    # id: int
    name: str
    description: str = ""
    price: float
    stock: int

with open("data/products.json") as f:
    products = json.load(f)
    f.close()


# products = []

def product_id(id):
    product, index = None, None
    for i, p in enumerate(products):
        if p["id"] == id:
            product, index = p, i
            break
    return index, product


def auto_id():
    if len(products) == 0:
        return 1
    p = products[-1]
    id = p["id"]
    id = id + 1
    return id

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/products")
def get_products():
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    return {"data": rows}

@app.get("/product/{id}")
def get_product(id: int):
    # product = None
    # for p in products:
    #     if p["id"] == id:
    #         product = p
    product = product_id(id)[1]

    # if not product:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"product with id {id} was not found"}
            
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} was not found")
    
    return {"product": product}


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_product(new_product: Product):
    print(new_product.model_dump())
    product_dict = new_product.model_dump()
    product_dict["id"] = auto_id()
    # products.append(new_product.model_dump())
    # print(products)
    products.append(product_dict)
    return {"message": product_dict}


@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = None
    index = product_id(id)[0]

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    products.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/product/{id}")
def update_product(id: int, product: Product):
    index = product_id(id)[0]

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    prod_dict = product.model_dump()
    prod_dict["id"] = id
    products[index] = prod_dict

    return {"procuct": prod_dict}



