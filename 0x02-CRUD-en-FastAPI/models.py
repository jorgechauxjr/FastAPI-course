from pydantic import BaseModel
from sqlmodel import SQLModel

class CustomerBase(SQLModel):
    name: str
    description: str | None
    email: str
    age: int

class CreateCustomer(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
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