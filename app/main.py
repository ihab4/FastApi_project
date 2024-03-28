from os import getenv
from time import sleep
from typing import List

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

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


@app.get("/")
def root():
    return {"message": "Hello World"}


#get all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    # cur.execute("SELECT * FROM products")
    # rows = cur.fetchall()

    products = db.query(models.Product).all()
    return products

#get product by id
@app.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db)):

    # cur.execute("SELECT * FROM products WHERE id = %s", (str(id),))
    # product = cur.fetchone()

    product = db.query(models.Product).filter(models.Product.id == id).first()
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id {id} does not exists")
    
    return product

#create new product
@app.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)
def create_product(new_product: schemas.CreateProduct, db: Session = Depends(get_db)):

    # cur.execute("""INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s) RETURNING *""",
    #             (new_product.name, new_product.description, new_product.price, new_product.stock))
    # product = cur.fetchone()
    # conn.commit()

    product_dict = new_product.model_dump()
    # product = models.Product(name = new_product.name, description = new_product.description,
    #                         price = new_product.price, stock = new_product.stock)
    product = models.Product(**product_dict)
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

#delete product
@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cur.execute("DELETE FROM products WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cur.fetchone()
    # conn.commit()

    product = db.query(models.Product).filter(models.Product.id == id)

    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
#update product
@app.put("/product/{id}")
def update_product(id: int, product: schemas.UpdateProduct, db: Session = Depends(get_db)):

    # cur.execute("""UPDATE products SET name = %s, description = %s, price = %s, stock = %s WHERE id = %s 
    #             RETURNING *""", (product.name, product.description, product.price, product.stock, str(id)))
    # updated_product = cur.fetchone()
    # conn.commit()

    product_query = db.query(models.Product).filter(models.Product.id == id)

    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {id} does not exists")

    product_query.update(product.model_dump(), synchronize_session=False)
    db.commit()

    return product_query.first()

#***********************************************************************
#SELLERS

@app.post("/seller", status_code=status.HTTP_201_CREATED)
def create_product(new_seller: schemas.CreateSeller, db: Session = Depends(get_db)):

    seller_dict = new_seller.model_dump()

    seller = models.Seller(**seller_dict)
    db.add(seller)
    db.commit()
    db.refresh(seller)

    return seller

@app.get("/sellers", response_model=List[schemas.SellerResponse])
def get_sellers(db: Session = Depends(get_db)):
    sellers = db.query(models.Seller).all()

    return sellers

@app.get("/seller/{id}", response_model=schemas.SellerResponse)
def get_seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id).first()

    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    return seller

@app.put("/seller/{id}")
def update_seller(id: int, seller: schemas.CreateSeller, db: Session = Depends(get_db)):
    seller_query = db.query(models.Seller).filter(models.Seller.id == id)

    if not seller_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    seller_query.update(seller.model_dump(), synchronize_session=False)

    db.commit()

    return seller_query.first()

@app.put("/password/{id}")
def change_password(id: int, seller: schemas.ChangePassword, db: Session = Depends(get_db)):
    seller_query = db.query(models.Seller).filter(models.Seller.id == id)

    if not seller_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    seller_query.update(seller.model_dump(), synchronize_session=False)

    db.commit()

    return seller_query.first()

@app.delete("/seller/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seller(id: int, db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.id == id)

    if not seller.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"seller with id {id} does not exist")
    
    seller.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
