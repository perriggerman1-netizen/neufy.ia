from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Esto le permite al formulario hablarle al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Este es el molde de los datos que esperamos recibir
class Lead(BaseModel):
    nombre: str
    negocio: str
    whatsapp: str
    plan: str

@app.get("/hola")
def hola():
    return {"mensaje": "Hola, soy el backend de Neufy"}

@app.post("/leads")
def crear_lead(lead: Lead):
    # Leer los leads existentes
    if os.path.exists("leads.json"):
        with open("leads.json", "r") as f:
            leads = json.load(f)
    else:
        leads = []

    # Agregar el nuevo lead
    leads.append(lead.dict())

    # Guardar todos los leads
    with open("leads.json", "w") as f:
        json.dump(leads, f, indent=2)

    return {"mensaje": "Lead guardado correctamente"}