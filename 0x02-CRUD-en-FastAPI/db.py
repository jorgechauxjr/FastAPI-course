from typing import Annotated
from fastapi import Depends

#Nos permite crear una sesion para conectarnos a la base de datos
from sqlmodel import Session, create_engine



sqlite_name="db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def get_session():
    with Session(engine) as session:
        yield session

# Registrar la sesion como una dependencia para todos nuestros endpoints
SessionDep = Annotated[Session, Depends(get_session)]