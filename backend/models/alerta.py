from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoAlerta(str, enum.Enum):
    inasistencia = "inasistencia"
    inactividad_virtual = "inactividad_virtual"
    bajo_rendimiento = "bajo_rendimiento"

class EstadoAlerta(str, enum.Enum):
    pendiente = "pendiente"
    enviada = "enviada"
    vista = "vista"

class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    tipo = Column(Enum(TipoAlerta), nullable=False)
    estado = Column(Enum(EstadoAlerta), default=EstadoAlerta.pendiente)
    descripcion = Column(String, nullable=False)
    curso = Column(String, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_envio = Column(DateTime(timezone=True), nullable=True)

    estudiante = relationship("Estudiante", back_populates="alertas")