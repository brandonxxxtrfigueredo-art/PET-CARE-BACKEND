from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Veterinaria, Profesional, Producto
from app.schemas.schemas import (
    VeterinariaCreate, VeterinariaResponse,
    ProfesionalCreate, ProfesionalResponse,
    ProductoCreate, ProductoResponse
)

router = APIRouter(prefix="/veterinarias", tags=["Veterinarias & Catálogo"])

# --- VETERINARIAS ---
@router.post("/", response_model=VeterinariaResponse)
def crear_veterinaria(vet: VeterinariaCreate, db: Session = Depends(get_db)):
    """Crea una nueva clínica veterinaria en la plataforma."""
    nueva_vet = Veterinaria(**vet.model_dump())
    db.add(nueva_vet)
    db.commit()
    db.refresh(nueva_vet)
    return nueva_vet

@router.get("/", response_model=List[VeterinariaResponse])
def listar_veterinarias(db: Session = Depends(get_db)):
    """Lista todas las clínicas veterinarias registradas."""
    return db.query(Veterinaria).all()

# --- PROFESIONALES ---
@router.post("/{id_veterinaria}/profesionales", response_model=ProfesionalResponse)
def agregar_profesional(id_veterinaria: int, prof: ProfesionalCreate, db: Session = Depends(get_db)):
    """Agrega un profesional (veterinario) a una clínica específica."""
    vet = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinaria no encontrada")
    
    nuevo_prof = Profesional(**prof.model_dump(), id_veterinaria=id_veterinaria)
    db.add(nuevo_prof)
    db.commit()
    db.refresh(nuevo_prof)
    return nuevo_prof

@router.get("/{id_veterinaria}/profesionales", response_model=List[ProfesionalResponse])
def listar_profesionales(id_veterinaria: int, db: Session = Depends(get_db)):
    """Lista los profesionales que trabajan en una clínica específica."""
    return db.query(Profesional).filter(Profesional.id_veterinaria == id_veterinaria).all()

# --- PRODUCTOS ---
@router.post("/{id_veterinaria}/productos", response_model=ProductoResponse)
def agregar_producto(id_veterinaria: int, prod: ProductoCreate, db: Session = Depends(get_db)):
    """Agrega un producto al inventario de una clínica específica."""
    vet = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()
    if not vet:
        raise HTTPException(status_code=404, detail="Veterinaria no encontrada")
    
    nuevo_prod = Producto(**prod.model_dump(), id_veterinaria=id_veterinaria)
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)
    return nuevo_prod

@router.get("/{id_veterinaria}/productos", response_model=List[ProductoResponse])
def listar_productos(id_veterinaria: int, db: Session = Depends(get_db)):
    """Lista los productos disponibles en una clínica específica."""
    return db.query(Producto).filter(Producto.id_veterinaria == id_veterinaria).all()