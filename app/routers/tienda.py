from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Usuario, Carrito, DetalleCarrito, Producto, Pedido
from app.schemas.schemas import AgregarCarritoRequest, PedidoResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/tienda", tags=["E-Commerce"])

@router.post("/carrito/agregar")
def agregar_al_carrito(req: AgregarCarritoRequest, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    producto = db.query(Producto).filter(Producto.id_producto == req.id_producto).first()
    if not producto or producto.stock < req.cantidad:
        raise HTTPException(status_code=400, detail="Producto sin stock suficiente.")

    carrito = db.query(Carrito).filter(Carrito.id_usuario == usuario.id_usuario, Carrito.activo == True).first()
    if not carrito:
        carrito = Carrito(id_usuario=usuario.id_usuario)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)

    detalle = db.query(DetalleCarrito).filter(DetalleCarrito.id_carrito == carrito.id_carrito, DetalleCarrito.id_producto == req.id_producto).first()
    if detalle:
        detalle.cantidad += req.cantidad
    else:
        nuevo_detalle = DetalleCarrito(id_carrito=carrito.id_carrito, id_producto=req.id_producto, cantidad=req.cantidad)
        db.add(nuevo_detalle)
    
    db.commit()
    return {"mensaje": "Producto agregado exitosamente"}

@router.post("/checkout", response_model=PedidoResponse)
def procesar_compra(direccion: str, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    carrito = db.query(Carrito).filter(Carrito.id_usuario == usuario.id_usuario, Carrito.activo == True).first()
    if not carrito or not carrito.detalles:
        raise HTTPException(status_code=400, detail="El carrito está vacío.")

    total_pagar = 0.0
    for detalle in carrito.detalles:
        producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
        if producto.stock < detalle.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre}")
        
        total_pagar += (producto.precio * detalle.cantidad)
        producto.stock -= detalle.cantidad 

    nuevo_pedido = Pedido(
        id_usuario=usuario.id_usuario,
        total=total_pagar,
        direccion_entrega=direccion
    )
    db.add(nuevo_pedido)
    carrito.activo = False 
    db.commit()
    db.refresh(nuevo_pedido)
    
    return nuevo_pedido

@router.get("/pedidos", response_model=List[PedidoResponse])
def mis_pedidos(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    return db.query(Pedido).filter(Pedido.id_usuario == usuario.id_usuario).order_by(Pedido.fecha_compra.desc()).all()