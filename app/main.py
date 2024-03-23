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

#connecting to database
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


@app.get("/")
def root():
    return {"message": "Hello World"}


#get all products
@app.get("/products")
def get_products():
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    return {"data": rows}

#get product by id
@app.get("/product/{id}")
def get_product(id: int):

    cur.execute("SELECT * FROM products WHERE id = %s", (str(id),))
    product = cur.fetchone()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} does not exists")
    
    return {"product": product}

#create new product
@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_product(new_product: Product):

    cur.execute("""INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s) RETURNING *""",
                (new_product.name, new_product.description, new_product.price, new_product.stock))
    product = cur.fetchone()
    conn.commit()
    return {"message": product}

#delete product
@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cur.execute("DELETE FROM products WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cur.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update product
@app.put("/product/{id}")
def update_product(id: int, product: Product):

    cur.execute("""UPDATE products SET name = %s, description = %s, price = %s, stock = %s WHERE id = %s 
                RETURNING *""", (product.name, product.description, product.price, product.stock, str(id)))
    updated_product = cur.fetchone()
    conn.commit()

    if updated_product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    return {"procuct": updated_product}
