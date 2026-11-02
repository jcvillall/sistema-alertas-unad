from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine
from models import estudiante, alerta, consentimiento, registro_academico
from routers import estudiantes, alertas, evaluacion, notificaciones
from tasks.scheduler import iniciar_scheduler, detener_scheduler

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_scheduler()
    yield
    detener_scheduler()

app = FastAPI(title="Sistema de Alertas UNAD", version="1.0.0", lifespan=lifespan)

app.include_router(estudiantes.router)
app.include_router(alertas.router)
app.include_router(evaluacion.router)
app.include_router(notificaciones.router)

@app.get("/")
def root():
    return {"mensaje": "Sistema de Alertas Tempranas UNAD", "estado": "activo"}

@app.get("/health")
def health():
    return {"estado": "ok", "base_de_datos": "conectada"}