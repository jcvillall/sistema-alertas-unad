from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    environment: str = "development"

    # Umbrales configurables del motor de alertas
    umbral_asistencia: float = 0.80      # menos de 80% de asistencia genera alerta
    dias_inactividad_max: int = 7        # más de 7 días sin ingresar al aula genera alerta
    nota_minima: float = 3.0             # nota por debajo de 3.0 genera alerta

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()