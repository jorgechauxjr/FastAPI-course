from typing import Annotated
from fastapi import Depends, FastAPI

#Nos permite crear una sesion para conectarnos a la base de datos
from sqlmodel import Session, create_engine, SQLModel



sqlite_name="db.sqlite3"
sqlite_url = f"sqlite:///0x02-CRUD-en-FastAPI/{sqlite_name}"

engine = create_engine(sqlite_url)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    print("Base de datos creada!")
    yield

def get_session():
    with Session(engine) as session:
        yield session

# Registrar la sesion como una dependencia para todos nuestros endpoints
SessionDep = Annotated[Session, Depends(get_session)]