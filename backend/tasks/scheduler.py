import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from config import get_settings
from database import SessionLocal
from services.motor_alertas import ejecutar_evaluacion
from services.notificador import notificar_pendientes

logger = logging.getLogger("uvicorn.error")
scheduler = BackgroundScheduler(timezone="America/Bogota")

def ciclo_completo():
    """Evalúa el riesgo académico y notifica las alertas pendientes."""
    db = SessionLocal()
    try:
        evaluacion = ejecutar_evaluacion(db)
        notificacion = notificar_pendientes(db)
        logger.info(f"Ciclo automático | evaluación: {evaluacion} | notificación: {notificacion}")
    except Exception as e:
        logger.error(f"Error en el ciclo automático: {e}")
    finally:
        db.close()

def iniciar_scheduler():
    s = get_settings()
    if not s.scheduler_activo:
        return
    if s.scheduler_intervalo_minutos > 0:
        scheduler.add_job(
            ciclo_completo, "interval",
            minutes=s.scheduler_intervalo_minutos,
            id="ciclo_alertas", replace_existing=True,
        )
    else:
        scheduler.add_job(
            ciclo_completo, CronTrigger(hour=s.scheduler_hora, minute=0),
            id="ciclo_alertas", replace_existing=True,
        )
    scheduler.start()

def detener_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)