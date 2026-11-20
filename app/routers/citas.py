from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Usuario, Mascota, CitaVeterinaria, Medicamento
from app.schemas.schemas import CitaCreate, CitaResponse, MedicamentoCreate, MedicamentoResponse
from app.core.security import get_current_user

# Cambiamos el prefijo y el tag
router = APIRouter(prefix="/citas", tags=["Citas y Salud Veterinaria"])

@router.post("/", response_model=CitaResponse)
def agendar_cita(cita: CitaCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    mascota = db.query(Mascota).filter(Mascota.id_mascota == cita.id_mascota, Mascota.id_usuario == usuario.id_usuario).first()
    if not mascota:
        raise HTTPException(status_code=403, detail="La mascota no existe o no te pertenece.")
    
    nueva_cita = CitaVeterinaria(**cita.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita

@router.get("/", response_model=List[CitaResponse])
def mis_citas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    mascotas_ids = [m.id_mascota for m in usuario.mascotas]
    return db.query(CitaVeterinaria).filter(CitaVeterinaria.id_mascota.in_(mascotas_ids)).all()

@router.post("/mascotas/{id_mascota}/medicamentos", response_model=MedicamentoResponse)
def recetar_medicamento(id_mascota: int, med: MedicamentoCreate, db: Session = Depends(get_db)):
    nuevo_med = Medicamento(**med.model_dump(), id_mascota=id_mascota)
    db.add(nuevo_med)
    db.commit()
    db.refresh(nuevo_med)
    return nuevo_med