from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.estudiante import Estudiante
from schemas.estudiante import EstudianteCreate, EstudianteResponse, EstudianteUpdate

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.get("/", response_model=List[EstudianteResponse])
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

@router.post("/", response_model=EstudianteResponse)
def crear_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    db_estudiante = db.query(Estudiante).filter(
        Estudiante.codigo == estudiante.codigo
    ).first()
    if db_estudiante:
        raise HTTPException(status_code=400, detail="El código ya existe")
    nuevo = Estudiante(**estudiante.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(estudiante_id: int, datos: EstudianteUpdate, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(estudiante, campo, valor)
    db.commit()
    db.refresh(estudiante)
    return estudiante

@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}