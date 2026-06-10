import zoneinfo
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from models import CreateCustomer, Customer, Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select

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
    session.add(customer)
    session.commit()
    session.refresh(customer)
    
    return customer

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    return customer_db

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exists")
    session.delete(customer_db)
    session.commit()
    return { "detail": "ok" }

@app.get("/customers", response_model=list[Customer])
async def list_customer(session: SessionDep):
    return session.exec(select(Customer)).all() # Devuelve una lista

@app.get("/customers/{customer_id}", response_model=Customer)
async def list_customer_by_id(customer_id: int):
    for customer in db_customers:
        if customer.id == customer_id:
            return customer
        
@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: CreateCustomer, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer does not exist")
    customer_db.name = customer_data.name
    customer_db.description = customer_data.description
    customer_db.email = customer_data.email
    customer_db.age = customer_data.age
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

