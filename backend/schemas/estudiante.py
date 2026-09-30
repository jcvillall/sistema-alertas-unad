from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EstudianteBase(BaseModel):
    codigo: str
    nombre: str
    apellido: str
    correo_institucional: str
    correo_personal: Optional[str] = None
    telefono: Optional[str] = None
    programa: Optional[str] = None

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    correo_personal: Optional[str] = None
    telefono: Optional[str] = None
    programa: Optional[str] = None
    activo: Optional[bool] = None

class EstudianteResponse(EstudianteBase):
    id: int
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True