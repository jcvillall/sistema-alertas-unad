from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.notificador import notificar_pendientes

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

@router.post("/enviar-pendientes")
def enviar_pendientes(db: Session = Depends(get_db)):
    return notificar_pendientes(db)