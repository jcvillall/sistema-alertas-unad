from fastapi import FastAPI

app = FastAPI(title="Sistema de Alertas UNAD", version="1.0.0")

@app.get("/")
def root():
    return {"mensaje": "Sistema de Alertas Tempranas UNAD", "estado": "activo"}