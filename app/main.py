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

    cur.execute("SELECT * FROM products WHERE id = %s", (str(id),))
    product = cur.fetchone()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} does not exists")
    
    return {"product": product}


@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_product(new_product: Product):

    cur.execute("""INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s) RETURNING *""",
                (new_product.name, new_product.description, new_product.price, new_product.stock))
    product = cur.fetchone()
    conn.commit()
    return {"message": product}


@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cur.execute("DELETE FROM products WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

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



