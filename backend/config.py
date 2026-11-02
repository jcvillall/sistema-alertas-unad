from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    environment: str = "development"

    # Umbrales configurables del motor de alertas
    umbral_asistencia: float = 0.80
    dias_inactividad_max: int = 7
    nota_minima: float = 3.0

    # Notificaciones por correo ("consola" o "smtp")
    email_modo: str = "consola"
    email_remitente: str = "alertas@sistema-alertas.local"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_usuario: str = ""
    smtp_password: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()