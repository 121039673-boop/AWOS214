from fastapi import FastAPI, HTTPException, status  
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

# Instancia del servidor
app = FastAPI(
    title="API Repaso",
    description="Valeria Briones Patiño",
    version="2.0.0"
)

# Endpoint saludo
@app.get("/", tags=['inicio'])
async def bienvenida():
    return {"Bienvenido a la biblioteca digital"}

