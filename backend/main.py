from fastapi import FastAPI
from database import Base, engine
from models import estudiante, alerta, consentimiento

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Alertas UNAD", version="1.0.0")

@app.get("/")
def root():
    return {"mensaje": "Sistema de Alertas Tempranas UNAD", "estado": "activo"}

@app.get("/health")
def health():
    return {"estado": "ok", "base_de_datos": "conectada"}