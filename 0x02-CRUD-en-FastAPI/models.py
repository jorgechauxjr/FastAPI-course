from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CreateCustomer(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
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