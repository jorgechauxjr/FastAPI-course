from pydantic import BaseModel

# 7 Validación de Datos y Modelos en Endpoints de FastAPI

class CustomerBase(BaseModel):
    name: str
    description: str | None
    email: str
    age: int

class CreateCustomer(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int | None = None
    
class Transaction(BaseModel):
    id: int
    amount: int
    description: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def total_amount(self):
        return sum(Transaction.amount for transaction in self.transactions)