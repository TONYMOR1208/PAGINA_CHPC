from flask import Blueprint, request, jsonify
from models import Producto
from schemas.producto_schema import ProductoSchema
from app import db

bp = Blueprint('producto_routes', __name__, url_prefix='/productos')

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

@bp.route('/', methods=['POST'])
def crear_producto():
    data = request.json
    errors = producto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

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
    db.session.add(nuevo_producto)
    db.session.commit()
    return producto_schema.jsonify(nuevo_producto), 201

@bp.route('/', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return productos_schema.jsonify(productos), 200

@bp.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get_or_404(id)
    return producto_schema.jsonify(producto), 200

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.json
    errors = producto_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    producto.peso = data.get('peso', producto.peso)
    producto.color = data.get('color', producto.color)
    producto.volumen = data.get('volumen', producto.volumen)
    producto.id_categoria = data.get('id_categoria', producto.id_categoria)
    producto.id_marca = data.get('id_marca', producto.id_marca)
    db.session.commit()
    return producto_schema.jsonify(producto), 200

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado exitosamente"}), 200
