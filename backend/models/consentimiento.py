from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Consentimiento(Base):
    __tablename__ = "consentimientos"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    correo_personal = Column(Boolean, default=False)
    sms = Column(Boolean, default=False)
    whatsapp = Column(Boolean, default=False)
    fecha_aceptacion = Column(DateTime(timezone=True), server_default=func.now())
    ip_aceptacion = Column(String, nullable=True)

    estudiante = relationship("Estudiante", back_populates="consentimiento")