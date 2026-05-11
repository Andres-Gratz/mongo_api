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
client = MongoClient("")

# TODO: Especificar el nombre de la base de datos asignada
# db = client["ISIS*******"]
db = client[""]

# ==========================================
# Endpoints
# ==========================================

@app.get("/")
def inicio():
    """Endpoint de verificación de estado."""
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    """Retorna la lista de comentarios asociados a un bar."""
    comentarios = None  # TODO: Completar la consulta
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    """Crea un nuevo comentario para un bar específico."""
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
    # TODO: Insertar el comentario en la base de datos
    return {'mensaje': 'Comentario guardado'}

# TODO: Implementar GET /bares/{bar_id}/eventos
# Retornar todos los eventos de un bar desde la colección 'eventos'

# TODO: Implementar POST /bares/{bar_id}/eventos  
# Insertar un evento en la colección 'eventos'
# Nota: Agregar 'bar_id' y 'fecha_creacion' al documento antes de guardarlo