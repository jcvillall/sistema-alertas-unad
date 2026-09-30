from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.alerta import TipoAlerta, EstadoAlerta

class AlertaBase(BaseModel):
    estudiante_id: int
    tipo: TipoAlerta
    descripcion: str
    curso: Optional[str] = None

class AlertaCreate(AlertaBase):
    pass

class AlertaResponse(AlertaBase):
    id: int
    estado: EstadoAlerta
    fecha_creacion: datetime
    fecha_envio: Optional[datetime] = None

    class Config:
        from_attributes = True