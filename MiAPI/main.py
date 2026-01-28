from fastapi import FastAPI
import asyncio

#Instancia del servidor
app = FastAPI()

@app.get("/")
async def bienvenida():
   return {"mensaje": "¡Bienvenido a mi API!"}

@app.get("/HolaMundo") #Endpoint
async def hola():
      await asyncio.sleep(3)
      return {"mensaje": "Hola Mundo FastAPI",
         "estatus":"200"
      } #FORMATO JSON

      