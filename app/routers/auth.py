from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioResponse, Token
from app.crud import crud
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_by_correo(db, usuario.correo_electronico):
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    return crud.create_usuario(db, usuario)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_correo(db, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token(data={"sub": str(usuario.id_usuario)})
    return Token(access_token=token)
