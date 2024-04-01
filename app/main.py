from os import getenv
from time import sleep

from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

from . import models
from .database import engine
from .routers import product, seller


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

app.include_router(product.router)
app.include_router(seller.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
