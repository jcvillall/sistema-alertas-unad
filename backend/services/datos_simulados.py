from datetime import datetime, timedelta, timezone
from database import SessionLocal
from models import estudiante, alerta, consentimiento  # necesarios para resolver relaciones
from models.estudiante import Estudiante
from models.registro_academico import Curso, Matricula

CURSOS = [
    ("301126", "Programación Orientada a Objetos", "virtual"),
    ("301127", "Bases de Datos", "virtual"),
    ("301128", "Redes de Computadores", "presencial"),
]

# (codigo, nombre, apellido, perfil)
ESTUDIANTES = [
    ("1001", "Ana", "Torres", "sano"),
    ("1002", "Luis", "Ramírez", "sano"),
    ("1003", "María", "Gómez", "sano"),
    ("1004", "Carlos", "Pérez", "sano"),
    ("1005", "Laura", "Díaz", "sano"),
    ("1006", "Andrés", "Mora", "inasistente"),
    ("1007", "Sofía", "Rojas", "inasistente"),
    ("1008", "Jorge", "Castro", "inactivo"),
    ("1009", "Paula", "Vargas", "inactivo"),
    ("1010", "Diego", "Herrera", "bajo_rendimiento"),
    ("1011", "Camila", "Ortiz", "bajo_rendimiento"),
    ("1012", "Felipe", "Navarro", "multiple"),
]

def valores_por_perfil(perfil, ahora):
    """Devuelve (nota, sesiones_asistidas, ultimo_acceso) según el perfil."""
    if perfil == "sano":
        return 4.2, 15, ahora - timedelta(days=1)
    if perfil == "inasistente":
        return 3.8, 9, ahora - timedelta(days=2)
    if perfil == "inactivo":
        return 3.9, 15, ahora - timedelta(days=12)
    if perfil == "bajo_rendimiento":
        return 2.1, 14, ahora - timedelta(days=2)
    return 1.8, 8, ahora - timedelta(days=15)  # multiple

def cargar():
    db = SessionLocal()
    try:
        ahora = datetime.now(timezone.utc)

        cursos = []
        for codigo, nombre, modalidad in CURSOS:
            curso = db.query(Curso).filter(Curso.codigo == codigo).first()
            if not curso:
                curso = Curso(codigo=codigo, nombre=nombre, modalidad=modalidad)
                db.add(curso)
                db.flush()
            cursos.append(curso)

        creados = 0
        for codigo, nombre, apellido, perfil in ESTUDIANTES:
            est = db.query(Estudiante).filter(Estudiante.codigo == codigo).first()
            if est:
                continue
            est = Estudiante(
                codigo=codigo,
                nombre=nombre,
                apellido=apellido,
                correo_institucional=f"{nombre.lower()}.{apellido.lower()}@sim.unad.edu.co".replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u"),
                programa="Ingeniería de Sistemas",
            )
            db.add(est)
            db.flush()

            nota, asistidas, acceso = valores_por_perfil(perfil, ahora)
            curso = cursos[creados % len(cursos)]
            db.add(Matricula(
                estudiante_id=est.id,
                curso_id=curso.id,
                nota_actual=nota,
                sesiones_totales=16,
                sesiones_asistidas=asistidas,
                ultimo_acceso_aula=acceso,
            ))
            creados += 1

        db.commit()
        print(f"Datos simulados cargados: {creados} estudiantes nuevos.")
    finally:
        db.close()

if __name__ == "__main__":
    cargar()