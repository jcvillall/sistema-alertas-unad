from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    modalidad = Column(String, default="virtual")  # virtual o presencial

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    nota_actual = Column(Float, nullable=True)           # escala 0 a 5
    sesiones_totales = Column(Integer, default=0)
    sesiones_asistidas = Column(Integer, default=0)
    ultimo_acceso_aula = Column(DateTime(timezone=True), nullable=True)

    estudiante = relationship("Estudiante")
    curso = relationship("Curso")