import zoneinfo
from datetime import datetime
from fastapi import FastAPI
from models import CreateCustomer, Customer, Transaction, Invoice
from db import SessionDep, create_all_tables

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def read_root():
    return {"message": "Hola mundo"}

@app.get("/hora")
async def current_time():
    full_time = datetime.now().time()
    return {
        "Hora Actual": full_time
    }

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima"
}

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CreateCustomer, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    # Asumiendo que se hace en la base de datos. Aquí es para efectos practicos.
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get("/customers/{customer_id}", response_model=Customer)
async def list_customer_by_id(customer_id: int):
    for customer in db_customers:
        if customer.id == customer_id:
            return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

