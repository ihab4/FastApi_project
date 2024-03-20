import psycopg2
from psycopg2.extras import RealDictCursor

import json
import time
import os
from dotenv import load_dotenv


load_dotenv()

db_name, username, password, host = os.getenv("db_name"), os.getenv("username"), os.getenv("password"), os.getenv("host")

# Connect to PostgreSQL
while True:
    try:
        conn = psycopg2.connect(dbname=db_name, user=username, password=password,
                                host=host, port="5432", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull.")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


