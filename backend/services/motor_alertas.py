from datetime import datetime, timezone
from sqlalchemy.orm import Session
from config import get_settings
from models.alerta import Alerta, TipoAlerta, EstadoAlerta
from models.registro_academico import Matricula
from datetime import timedelta

def evaluar_matricula(m: Matricula, ahora: datetime):
    """Devuelve la lista de (tipo, descripcion) que aplican a una matrícula."""
    s = get_settings()
    hallazgos = []
    curso = m.curso.nombre

    # 1. Inasistencia
    if m.sesiones_totales and m.sesiones_totales > 0:
        asistencia = m.sesiones_asistidas / m.sesiones_totales
        if asistencia < s.umbral_asistencia:
            hallazgos.append((
                TipoAlerta.inasistencia,
                f"Asistencia del {asistencia:.0%} en {curso}, por debajo del {s.umbral_asistencia:.0%} requerido",
            ))

    # 2. Inactividad en aula virtual (solo cursos virtuales)
    if m.curso.modalidad == "virtual":
        if m.ultimo_acceso_aula is None:
            hallazgos.append((
                TipoAlerta.inactividad_virtual,
                f"Sin ingresos registrados al aula virtual de {curso}",
            ))
        else:
            dias = (ahora - m.ultimo_acceso_aula).days
            if dias > s.dias_inactividad_max:
                hallazgos.append((
                    TipoAlerta.inactividad_virtual,
                    f"{dias} días sin ingresar al aula virtual de {curso}",
                ))

    # 3. Bajo rendimiento
    if m.nota_actual is not None and m.nota_actual < s.nota_minima:
        hallazgos.append((
            TipoAlerta.bajo_rendimiento,
            f"Nota actual de {m.nota_actual} en {curso}, inferior al mínimo de {s.nota_minima}",
        ))

    return hallazgos

def ejecutar_evaluacion(db: Session):
    """Evalúa todas las matrículas y crea alertas nuevas sin duplicar."""
    ahora = datetime.now(timezone.utc)
    limite = ahora - timedelta(days=get_settings().dias_entre_alertas)
    matriculas = db.query(Matricula).all()
    creadas = 0
    omitidas = 0

    for m in matriculas:
        for tipo, descripcion in evaluar_matricula(m, ahora):
            existente = db.query(Alerta).filter(
                Alerta.estudiante_id == m.estudiante_id,
                Alerta.tipo == tipo,
                Alerta.curso == m.curso.nombre,
                Alerta.fecha_creacion >= limite,
            ).first()
            if existente:
                omitidas += 1
                continue
            db.add(Alerta(
                estudiante_id=m.estudiante_id,
                tipo=tipo,
                descripcion=descripcion,
                curso=m.curso.nombre,
            ))
            creadas += 1

    db.commit()
    return {
        "matriculas_evaluadas": len(matriculas),
        "alertas_creadas": creadas,
        "alertas_omitidas_por_duplicado": omitidas,
    }