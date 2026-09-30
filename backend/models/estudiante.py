from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo_institucional = Column(String, unique=True, nullable=False)
    correo_personal = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    programa = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())

    alertas = relationship("Alerta", back_populates="estudiante")
    consentimiento = relationship("Consentimiento", back_populates="estudiante", uselist=False)