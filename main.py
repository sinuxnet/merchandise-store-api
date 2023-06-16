import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

# Get the database credentials from environment variables
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Establish a connection to the database
conn = psycopg2.connect(
    host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()


# Endpoint to retrieve all products
@app.get("/products")
async def get_all_products():
    # Execute a SELECT query
    cur.execute("SELECT * FROM products")

    # Fetch all rows from the result set
    rows = cur.fetchall()

    # Convert the rows to a list of dictionaries
    product_list = []
    for row in rows:
        product_dict = {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
        }
        product_list.append(product_dict)

    return JSONResponse(content=product_list)


# Endpoint to retrieve a specific product by ID
@app.get("/products/{product_id}")
async def get_product_by_id(product_id: int):
    # Execute a SELECT query with a parameterized query string
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))

    # Fetch the row for the specified product ID
    product = cur.fetchone()

    # If no product is found, raise an HTTPException with a 404 status code
    if not product:
        error_message = {
            "error": "Product not found",
            "product_id": product_id,
            "message": "The requested product could not be found.",
            "suggestions": [
                "Double-check the product ID and try again.",
                "Ensure the product exists in the database.",
                "Contact support for further assistance."
            ]
        }
        raise HTTPException(status_code=404, detail=error_message)

    # Convert the row to a dictionary representing the product
    product_dict = {
        "id": product[0],
        "name": product[1],
        "price": product[2],
        "description": product[3],
    }

    return JSONResponse(content=product_dict)