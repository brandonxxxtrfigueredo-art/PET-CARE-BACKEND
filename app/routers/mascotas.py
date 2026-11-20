from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.schemas import MascotaResponse, MascotaCreate
from app.models.models import Usuario
from app.crud import crud
from app.core.security import get_current_user

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])

@router.get("/", response_model=List[MascotaResponse])
def listar_mis_mascotas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    return crud.get_mascotas_by_usuario(db, usuario.id_usuario)

@router.post("/", response_model=MascotaResponse)
def registrar_mascota(mascota: MascotaCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    return crud.create_mascota(db, mascota, usuario.id_usuario)
