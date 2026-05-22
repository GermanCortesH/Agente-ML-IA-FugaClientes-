from fastapi import FastAPI
import uvicorn
from data.repositorio_cliente import get_customer_by_id
app = FastAPI()

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = get_customer_by_id(customer_id)
    return customer

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)