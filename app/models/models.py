from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    correo_electronico = Column(String(100), nullable=False, unique=True, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    rol = Column(String(20), nullable=False, default="cliente")
    activo = Column(Boolean, nullable=False, default=True)
    mascotas = relationship("Mascota", back_populates="dueno")
    pedidos = relationship("Pedido", back_populates="usuario")

class Mascota(Base):
    __tablename__ = "mascotas"
    id_mascota = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    nombre = Column(String(50), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50))
    peso = Column(Float)
    fecha_nacimiento = Column(Date)
    numero_chip = Column(String(50), unique=True)
    alergias = Column(Text)
    condiciones_medicas = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    dueno = relationship("Usuario", back_populates="mascotas")
    citas = relationship("CitaVeterinaria", back_populates="mascota")
    medicamentos = relationship("Medicamento", back_populates="mascota")

class Veterinaria(Base):
    __tablename__ = "veterinarias"
    id_veterinaria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(Text, nullable=False)
    telefono = Column(String(20))
    latitud = Column(Float)
    longitud = Column(Float)
    calificacion_promedio = Column(Float, default=0.0)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    profesionales = relationship("Profesional", back_populates="veterinaria")
    productos = relationship("Producto", back_populates="veterinaria")

class Profesional(Base):
    __tablename__ = "profesionales"
    id_profesional = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"))
    nombre_completo = Column(String(100), nullable=False)
    especialidad = Column(String(100))
    numero_registro = Column(String(50))
    activo = Column(Boolean, default=True)
    veterinaria = relationship("Veterinaria", back_populates="profesionales")

class CitaVeterinaria(Base):
    __tablename__ = "citas_veterinarias"
    id_cita = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"))
    id_profesional = Column(Integer, ForeignKey("profesionales.id_profesional"))
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"))
    fecha_hora = Column(DateTime(timezone=True), nullable=False)
    motivo = Column(Text)
    estado = Column(String(20), default="programada")
    mascota = relationship("Mascota", back_populates="citas")

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"))
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    veterinaria = relationship("Veterinaria", back_populates="productos")

class Medicamento(Base):
    __tablename__ = "medicamentos"
    id_medicamento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"))
    nombre = Column(String(100), nullable=False)
    dosis = Column(String(100))
    frecuencia = Column(String(100))
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    mascota = relationship("Mascota", back_populates="medicamentos")

class Carrito(Base):
    __tablename__ = "carritos"
    id_carrito = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    activo = Column(Boolean, default=True)
    detalles = relationship("DetalleCarrito", back_populates="carrito")

class DetalleCarrito(Base):
    __tablename__ = "detalles_carrito"
    id_detalle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_carrito = Column(Integer, ForeignKey("carritos.id_carrito"))
    id_producto = Column(Integer, ForeignKey("productos.id_producto"))
    cantidad = Column(Integer, default=1)
    carrito = relationship("Carrito", back_populates="detalles")
    producto = relationship("Producto")

class Pedido(Base):
    __tablename__ = "pedidos"
    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    total = Column(Float, nullable=False)
    estado = Column(String(50), default="pagado")
    direccion_entrega = Column(Text)
    fecha_compra = Column(DateTime(timezone=True), server_default=func.now())
    usuario = relationship("Usuario", back_populates="pedidos")