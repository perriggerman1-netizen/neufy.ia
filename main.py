from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ── Conexión a PostgreSQL ──────────────────────────────
DATABASE_URL = "postgresql://postgres:auto898neuf@localhost:5432/Neufy"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ── Modelo de la tabla leads ───────────────────────────
class LeadDB(Base):
    __tablename__ = "leads"
    id       = Column(Integer, primary_key=True, index=True)
    nombre   = Column(String)
    negocio  = Column(String)
    whatsapp = Column(String)
    plan     = Column(String)
    fecha    = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

# ── App FastAPI ────────────────────────────────────────
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    db = SessionLocal()
    nuevo_lead = LeadDB(
        nombre=lead.nombre,
        negocio=lead.negocio,
        whatsapp=lead.whatsapp,
        plan=lead.plan
    )
    db.add(nuevo_lead)
    db.commit()
    db.close()
    return {"mensaje": "Lead guardado en PostgreSQL"}

@app.get("/leads")
def obtener_leads():
    db = SessionLocal()
    leads = db.query(LeadDB).all()
    db.close()

    resultado = []
    for lead in leads:
        resultado.append({
            "id": lead.id,
            "nombre": lead.nombre,
            "negocio": lead.negocio,
            "whatsapp": lead.whatsapp,
            "plan": lead.plan,
            "fecha": lead.fecha
        })

    return resultado-