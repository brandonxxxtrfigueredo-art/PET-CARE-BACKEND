from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime, date

# --- Usuarios e Identidad ---
class UsuarioBase(BaseModel):
    nombre_completo: str
    correo_electronico: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: int
    rol: str
    activo: bool
    fecha_registro: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Mascotas ---
class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    peso: Optional[float] = None
    fecha_nacimiento: Optional[date] = None
    numero_chip: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_medicas: Optional[str] = None

class MascotaCreate(MascotaBase):
    pass

class MascotaResponse(MascotaBase):
    model_config = ConfigDict(from_attributes=True)
    id_mascota: int
    id_usuario: int
    fecha_creacion: datetime

# --- Veterinarias y Productos ---
class VeterinariaBase(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class VeterinariaResponse(VeterinariaBase):
    model_config = ConfigDict(from_attributes=True)
    id_veterinaria: int
    calificacion_promedio: float

class ProductoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_producto: int
    nombre: str
    precio: float
    stock: int

# --- Clínica y Citas ---
class CitaCreate(BaseModel):
    id_mascota: int
    id_veterinaria: int
    id_profesional: int
    fecha_hora: datetime
    motivo: str

class CitaResponse(CitaCreate):
    model_config = ConfigDict(from_attributes=True)
    id_cita: int
    estado: str

class MedicamentoCreate(BaseModel):
    nombre: str
    dosis: str
    frecuencia: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class MedicamentoResponse(MedicamentoCreate):
    model_config = ConfigDict(from_attributes=True)
    id_medicamento: int
    id_mascota: int

# --- E-Commerce ---
class AgregarCarritoRequest(BaseModel):
    id_producto: int
    cantidad: int

class DetalleCarritoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    producto: ProductoResponse
    cantidad: int

class CarritoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_carrito: int
    detalles: List[DetalleCarritoResponse]
    total_estimado: float = 0.0

class PedidoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_pedido: int
    total: float
    estado: str
    direccion_entrega: str
    fecha_compra: datetime

# --- Modelos Administrativos (Creación) ---
class VeterinariaCreate(VeterinariaBase):
    pass

class ProfesionalBase(BaseModel):
    nombre_completo: str
    especialidad: Optional[str] = None
    numero_registro: Optional[str] = None

class ProfesionalCreate(ProfesionalBase):
    pass

class ProfesionalResponse(ProfesionalBase):
    model_config = ConfigDict(from_attributes=True)
    id_profesional: int
    id_veterinaria: int
    activo: bool

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0