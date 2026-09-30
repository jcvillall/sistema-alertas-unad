from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.alerta import Alerta, EstadoAlerta
from models.estudiante import Estudiante
from schemas.alerta import AlertaCreate, AlertaResponse
from datetime import datetime, timezone

router = APIRouter(prefix="/alertas", tags=["Alertas"])

@router.get("/", response_model=List[AlertaResponse])
def listar_alertas(db: Session = Depends(get_db)):
    return db.query(Alerta).all()

@router.get("/estudiante/{estudiante_id}", response_model=List[AlertaResponse])
def alertas_por_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db.query(Alerta).filter(Alerta.estudiante_id == estudiante_id).all()

@router.post("/", response_model=AlertaResponse)
def crear_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == alerta.estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    nueva = Alerta(**alerta.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/{alerta_id}/marcar-enviada", response_model=AlertaResponse)
def marcar_enviada(alerta_id: int, db: Session = Depends(get_db)):
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    alerta.estado = EstadoAlerta.enviada
    alerta.fecha_envio = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alerta)
    return alerta