from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, mascotas, veterinarias, citas, tienda 

app = FastAPI(
    title="PeludOS API Completa",
    description="API para la plataforma de cuidado de mascotas y veterinaria",
    version="1.0.0"
)

# Habilitar peticiones HTTP desde el origen de Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Integración de todos los módulos del sistema
app.include_router(auth.router)
app.include_router(mascotas.router)
app.include_router(veterinarias.router)
app.include_router(citas.router)
app.include_router(tienda.router)

@app.get("/health", tags=["Salud"])
def health_check():
    """
    Endpoint para verificar que el servidor está corriendo correctamente.
    """
    return {"status": "ok", "app": "PeludOS Backend Complete"}