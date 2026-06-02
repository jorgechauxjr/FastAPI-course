from pydantic import BaseModel

# 6. Modelo de datos y conexión de modelos en FastAPI

class Customer(BaseModel):
    id: int
    name: str
    description: str | None
    email: str
    age: int

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