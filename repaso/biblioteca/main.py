from fastapi import FastAPI, HTTPException, status  
import asyncio
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime
from models import Libro, Prestamo

libros = []
prestamos = []
current_year = datetime.now().year


# Instancia del servidor
app = FastAPI(
    title="API Repaso",
    description="Valeria Briones Patiño",
    version="2.0.0"
)

#Endpoint saludo
@app.get("/", tags=['inicio'])
async def bienvenida():
    return {"Bienvenido a la biblioteca digital"}


#Registrar libro
@app.post("/libros", status_code=201)
def registrar_libro(libro: Libro):
    for l in libros:
        if l.nombre.lower() == libro.nombre.lower():
            raise HTTPException(status_code=400, detail="Libro ya existe")
    libros.append(libro)
    return libro

#Listar libros
@app.get("/libros")
def listar_libros():
    return libros

#Buscar libro por nombre
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    for libro in libros:
        if libro.nombre.lower() == nombre.lower():
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#Registrar préstamo
@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):
    for libro in libros:
        if libro.nombre.lower() == prestamo.libro_nombre.lower():
            if libro.estado == "prestado":
                raise HTTPException(status_code=409, detail="Libro ya prestado")
            libro.estado = "prestado"
            prestamos.append(prestamo)
            return {"mensaje": "Préstamo registrado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#Marcar libro como devuelto
@app.put("/prestamos/{nombre}")
def devolver_libro(nombre: str):
    for prestamo in prestamos:
        if prestamo.libro_nombre.lower() == nombre.lower():
            for libro in libros:
                if libro.nombre.lower() == nombre.lower():
                    libro.estado = "disponible"
                    prestamos.remove(prestamo)
                    return {"mensaje": "Libro devuelto"}
    raise HTTPException(status_code=409, detail="Registro de préstamo no existe")

#Eliminar registro de préstamo
@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):
    for prestamo in prestamos:
        if prestamo.libro_nombre.lower() == nombre.lower():
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado"}
    raise HTTPException(status_code=409, detail="Registro de préstamo no existe")

#Validaciones

class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    año: int = Field(..., gt=1450, le=current_year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

class Prestamo(BaseModel):
    libro_nombre: str
    usuario: Usuario