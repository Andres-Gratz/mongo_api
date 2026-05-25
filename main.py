from datetime import datetime
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI()

# Configuración de CORS para permitir peticiones desde cualquier cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# Configuración de Base de Datos
# ==========================================

# NOTA: Para despliegue, utilice la variable de entorno MONGO_URI:
# client = MongoClient(os.environ["MONGO_URI"])

# TODO: Conectarse al cluster Admonsis para desarrollo local
# client = MongoClient("mongodb://<usuario>:<contraseña>@157.253.236.88:8087")
client = MongoClient(os.environ["MONGO_URI"])

# TODO: Especificar el nombre de la base de datos asignada
# db = client["ISIS*******"]
db = client["ISIS2304J06202610"]

# ==========================================
# Endpoints
# ==========================================

@app.get("/")
def inicio():
    """Endpoint de verificación de estado."""
    return {"estado": "API funcionando correctamente"}

@app.get("/hoteles/{hotel_id}/resenas")
def get_resenas(hotel_id: int):

    coleccion = db["resenas"]

    resultados = list(
        coleccion.find({
            "hotelId": hotel_id,
            "estado": "publicada"
        })
    )

    for r in resultados:
        r["_id"] = str(r["_id"])

    return resultados

@app.post("/hoteles/{hotel_id}/resenas")
def crear_resena(hotel_id: int, datos: dict):

    coleccion = db["resenas"]

    datos["hotelId"] = hotel_id
    datos["fechaCreacion"] = datetime.now().isoformat()
    datos["estado"] = "publicada"

    resultado = coleccion.insert_one(datos)

    return {
        "mensaje": "Reseña creada",
        "id": str(resultado.inserted_id)
    }
