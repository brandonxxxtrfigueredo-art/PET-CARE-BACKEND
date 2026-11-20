from sqlalchemy.orm import Session
from app.models.models import Usuario, Mascota, Veterinaria, Producto
from app.schemas.schemas import UsuarioCreate, MascotaCreate
from app.core.security import hash_password

def get_usuario_by_correo(db: Session, correo_electronico: str):
    return db.query(Usuario).filter(Usuario.correo_electronico == correo_electronico).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_user = Usuario(**usuario.model_dump(exclude={'contrasena'}), contrasena_hash=hash_password(usuario.contrasena))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_mascotas_by_usuario(db: Session, id_usuario: int):
    return db.query(Mascota).filter(Mascota.id_usuario == id_usuario).all()

def create_mascota(db: Session, mascota: MascotaCreate, id_usuario: int):
    db_mascota = Mascota(**mascota.model_dump(), id_usuario=id_usuario)
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def get_veterinarias(db: Session):
    return db.query(Veterinaria).all()

def get_productos_by_veterinaria(db: Session, id_veterinaria: int):
    return db.query(Producto).filter(Producto.id_veterinaria == id_veterinaria, Producto.activo == True).all()
