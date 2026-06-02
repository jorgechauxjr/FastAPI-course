from fastapi import FastAPI
from datetime import datetime
import zoneinfo

app = FastAPI()

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

# Cl 4. Crear un Endpoint Dinámico con FastAPI para Obtener Hora por País y Formato

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}
