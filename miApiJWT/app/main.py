#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# Instancia del servidor
app = FastAPI(
    title='Mi primer API ',
    description='Valeria Briones Patiño',
    version='1.0.0'
    )

#TB ficticia
usuarios = [
    {"id":1, "nombre" : "Juan", "edad":21},
    {"id":2, "nombre" : "Israel", "edad":21},
    {"id":3, "nombre" : "Sofi", "edad":21},
]

#Modelo de validacion Pydantic
class usuario_create(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(..., min_length=3,max_length=50,example="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad valida entre 1 y 123")

#Seguridad HTTP Basic

security = HTTPBasic()

def verificar_Peticion(credenciales: HTTPBasicCredentials=Depends(security)):
   userAuth = secrets.compare_digest(credenciales.username, "Valeria Briones")
   passAuth = secrets.compare_digest(credenciales.password, "2427")
   
   if not(userAuth and passAuth):
      raise HTTPException(
         status_code= status.HTTP_401_UNAUTHORIZED,
         detail= "Credenciales no autorizadas"
      )

   return credenciales.username


# TB ficticia
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]

#Modelo de validacion pydantic 
class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de ussuario") #tres puntos para obligatorio y gt para ser mayor de cero
    nombre: str =Field(..., min_length=3,max_length=50,example="Juanita")
    edad: int = Field(...,ge=1,le=123,description="Edad valida entre 1 y 123")
#Para que pase la validación minimo debe pasar esos tres parametros 


#Los modelos pydantic solo sirven para agregar y actualizar 


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
async def crear_usuario(usuario:usuario_create): #llega un usuario ya validado y pasa a ser un modelo
    for usr in usuarios:
        if usr["id"] == usuario.id: #cambio el usuario.get a usuario.id porque ya no es una lista, ya es un modelo 
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }
#documentar el redoc 

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id: 
            usr.update(usuario)
            return {"mensaje": "Usuario actualizado", "usuario": usr}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")
      
      
 
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int, userAuth= Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "mensaje": f"Usuario eliminado exitosamente {userAuth}",
                "usuarios_restantes": len(usuarios)
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"No se pudo eliminar: El usuario con ID {id} no existe"
    )
