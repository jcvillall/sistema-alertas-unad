import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from sqlalchemy.orm import Session
from config import get_settings
from models.alerta import Alerta, EstadoAlerta
from models.estudiante import Estudiante

LOG_DIR = Path("logs")

def enviar_correo(destino: str, asunto: str, cuerpo: str) -> None:
    s = get_settings()

    if s.email_modo == "consola":
        LOG_DIR.mkdir(exist_ok=True)
        registro = (
            f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Para: {destino}\n"
            f"Asunto: {asunto}\n{cuerpo}\n{'-' * 60}\n"
        )
        print(registro)
        with open(LOG_DIR / "correos_simulados.log", "a", encoding="utf-8") as f:
            f.write(registro)
        return

    msg = EmailMessage()
    msg["From"] = s.email_remitente
    msg["To"] = destino
    msg["Subject"] = asunto
    msg.set_content(cuerpo)
    with smtplib.SMTP(s.smtp_host, s.smtp_port) as servidor:
        servidor.starttls()
        servidor.login(s.smtp_usuario, s.smtp_password)
        servidor.send_message(msg)

def construir_mensaje(estudiante: Estudiante, alerta: Alerta):
    tipo = alerta.tipo.value.replace("_", " ")
    asunto = f"Alerta académica: {tipo}"
    cuerpo = (
        f"Hola {estudiante.nombre},\n\n"
        f"{alerta.descripcion}.\n\n"
        "Te recomendamos revisar tu situación académica y comunicarte con tu "
        "consejero o tutor para recibir acompañamiento.\n\n"
        "Sistema de Alertas Tempranas"
    )
    return asunto, cuerpo

def notificar_pendientes(db: Session):
    pendientes = db.query(Alerta).filter(Alerta.estado == EstadoAlerta.pendiente).all()
    alertas_notificadas = 0
    correos_enviados = 0
    fallidas = 0

    for alerta in pendientes:
        est = db.query(Estudiante).filter(Estudiante.id == alerta.estudiante_id).first()
        if not est:
            continue

        asunto, cuerpo = construir_mensaje(est, alerta)

        # El correo institucional siempre recibe la alerta.
        # El correo personal solo si el estudiante dio su consentimiento.
        destinos = [est.correo_institucional]
        c = est.consentimiento
        if c and c.correo_personal and est.correo_personal:
            destinos.append(est.correo_personal)

        try:
            for destino in destinos:
                enviar_correo(destino, asunto, cuerpo)
                correos_enviados += 1
        except Exception as e:
            fallidas += 1
            print(f"No se pudo enviar la alerta {alerta.id}: {e}")
            continue

        alerta.estado = EstadoAlerta.enviada
        alerta.fecha_envio = datetime.now(timezone.utc)
        alertas_notificadas += 1

    db.commit()
    return {
        "alertas_notificadas": alertas_notificadas,
        "correos_enviados": correos_enviados,
        "alertas_fallidas": fallidas,
    }