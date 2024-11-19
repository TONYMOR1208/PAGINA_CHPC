from flask import Blueprint, jsonify, request
from models import db, Producto
from schemas.producto_schema import ProductoSchema
from sqlalchemy.exc import IntegrityError

producto_bp = Blueprint('productos', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


# Obtener todos los productos
@producto_bp.route('/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    producto_schema = ProductoSchema(many=True)
    return create_response(data=producto_schema.dump(productos), message="Lista de productos obtenida")


# Obtener un producto específico por ID
@producto_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    producto_schema = ProductoSchema()
    return create_response(data=producto_schema.dump(producto), message="Producto obtenido")


# Crear un nuevo producto
@producto_bp.route('/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    producto_schema = ProductoSchema()
    errors = producto_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nuevo_producto = Producto(
        nombre_producto=data['nombre_producto'],
        descripcion=data.get('descripcion'),
        precio=data['precio'],
        stock=data['stock'],
        peso=data['peso'],
        color=data.get('color'),
        volumen=data.get('volumen'),
        id_categoria=data['id_categoria'],
        id_marca=data['id_marca']
    )
    try:
        db.session.add(nuevo_producto)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al crear el producto. Verifica las claves foráneas.", status="error", code=400)

    return create_response(data=producto_schema.dump(nuevo_producto), message="Producto creado", code=201)


# Actualizar un producto existente
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()
    producto_schema = ProductoSchema()
    errors = producto_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    producto.peso = data.get('peso', producto.peso)
    producto.color = data.get('color', producto.color)
    producto.volumen = data.get('volumen', producto.volumen)
    producto.id_categoria = data.get('id_categoria', producto.id_categoria)
    producto.id_marca = data.get('id_marca', producto.id_marca)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al actualizar el producto. Verifica las claves foráneas.", status="error", code=400)

    return create_response(data=producto_schema.dump(producto), message="Producto actualizado")


# Eliminar un producto
@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)

    if producto.media_producto or producto.reseñas_producto or producto.carrito_producto:
        return create_response(
            message="No se puede eliminar un producto que tiene medios, reseñas o está en un carrito.",
            status="error",
            code=400
        )

    db.session.delete(producto)
    db.session.commit()
    return create_response(message="Producto eliminado", code=204)
