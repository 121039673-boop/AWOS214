from fastapi import FastAPI, HTTPException, status  
import asyncio
from typing import Optional

# Instancia del servidor
app = FastAPI(
    title="Mi primer API Valeria",
    description="Valeria Briones Patiño",
    version="1.0.0"
)

# TB ficticia
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]

# Endpoints
@app.get("/", tags=['inicio'])
async def bienvenida():
    return {"mensaje": "Bienvenido a mi API"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(3) # simulacion de una peticion
    return {
        "mensaje": "Hola Mundo FastAPI!",
        "estatus": "200"
    }

#Tercera endpoint
@app.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])  
async def consultaUno(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            return {"Se encontro usuario": usuario}
    return {"mensaje": "Usuario no encontrado", "id": id}


#Cuarta endpoint
@app.get("/v1/usuarios/", tags=['Parametro Opcional'])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "No se proporciono id"}

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios), 
        "usuarios":usuarios
    }


@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }
    

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id: 
            usr.update(usuario)
            return {"mensaje": "Usuario actualizado", "usuario": usr}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")
      
