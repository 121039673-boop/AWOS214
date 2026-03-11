from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal
from datetime import datetime

app = FastAPI(title="Biblioteca Digital API")

# -----------------------------
# Base de datos simulada
# -----------------------------
libros = [
    {
        "nombre": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "anio": 1605,
        "paginas": 863,
        "estado": "disponible"
    },
    {
        "nombre": "Cien Años de Soledad",
        "autor": "Gabriel Garcia Marquez",
        "anio": 1967,
        "paginas": 471,
        "estado": "disponible"
    },
    {
        "nombre": "La Odisea",
        "autor": "Homero",
        "anio": 1614,
        "paginas": 541,
        "estado": "prestado"
    },
    {
        "nombre": "El Principito",
        "autor": "Antoine de Saint Exupery",
        "anio": 1943,
        "paginas": 96,
        "estado": "disponible"
    }
]

prestamos = [
    {
        "libro_nombre": "La Odisea",
        "usuario": {
            "nombre": "Carlos Perez",
            "correo": "carlos@example.com"
        }
    }
]

# -----------------------------
# Modelos Pydantic
# -----------------------------
current_year = datetime.now().year


class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr


class Libro(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    autor: str
    anio: int = Field(..., gt=1450, le=current_year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"


class Prestamo(BaseModel):
    libro_nombre: str
    usuario: Usuario


# -----------------------------
# Endpoints
# -----------------------------

# a) Registrar un libro
@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):

    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El libro ya está registrado"
            )

    libros.append(libro.dict())
    return {"mensaje": "Libro registrado", "libro": libro}


# b) Listar todos los libros
@app.get("/libros", response_model=List[Libro])
def listar_libros():
    return libros


# c) Buscar libro por nombre
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro

    raise HTTPException(status_code=404, detail="Libro no encontrado")


# d) Registrar préstamo de libro
@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):

    libro = next((l for l in libros if l["nombre"].lower() == prestamo.libro_nombre.lower()), None)

    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    if libro["estado"] == "prestado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El libro ya está prestado"
        )

    libro["estado"] = "prestado"

    registro = prestamo.dict()
    prestamos.append(registro)

    return {
        "mensaje": "Préstamo registrado",
        "prestamo": registro
    }


# e) Marcar libro como devuelto
@app.put("/prestamos/devolver/{nombre}")
def devolver_libro(nombre: str):

    prestamo = next((p for p in prestamos if p["libro_nombre"].lower() == nombre.lower()), None)

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El registro de préstamo no existe"
        )

    libro = next((l for l in libros if l["nombre"].lower() == nombre.lower()), None)

    if libro:
        libro["estado"] = "disponible"

    return {"mensaje": "Libro devuelto correctamente"}


# f) Eliminar registro de préstamo
@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):

    prestamo = next((p for p in prestamos if p["libro_nombre"].lower() == nombre.lower()), None)

    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El registro de préstamo no existe"
        )

    prestamos.remove(prestamo)

    return {"mensaje": "Registro de préstamo eliminado"}

#contenedor
#docker build -t biblioteca-api 
#docker run -p 8000:8000 biblioteca-api











