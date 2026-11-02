from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.motor_alertas import ejecutar_evaluacion

router = APIRouter(prefix="/evaluacion", tags=["Evaluación"])

@router.post("/ejecutar")
def ejecutar(db: Session = Depends(get_db)):
    return ejecutar_evaluacion(db)