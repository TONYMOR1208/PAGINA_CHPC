from flask import Blueprint, request, jsonify
from models import Carrito
from schemas.carrito_schema import CarritoSchema
from app import db

bp = Blueprint('carrito_routes', __name__, url_prefix='/carrito')

carrito_schema = CarritoSchema()
carritos_schema = CarritoSchema(many=True)

@bp.route('/', methods=['POST'])
def agregar_carrito():
    data = request.json
    errors = carrito_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_carrito = Carrito(
        id_cliente=data['id_cliente'],
        id_producto=data['id_producto'],
        cantidad=data['cantidad']
    )
    db.session.add(nuevo_carrito)
    db.session.commit()
    return carrito_schema.jsonify(nuevo_carrito), 201

@bp.route('/', methods=['GET'])
def obtener_carrito():
    carrito = Carrito.query.all()
    return carritos_schema.jsonify(carrito), 200

@bp.route('/<int:id>', methods=['GET'])
def obtener_item_carrito(id):
    item = Carrito.query.get_or_404(id)
    return carrito_schema.jsonify(item), 200

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_item_carrito(id):
    item = Carrito.query.get_or_404(id)
    data = request.json
    errors = carrito_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    item.id_cliente = data.get('id_cliente', item.id_cliente)
    item.id_producto = data.get('id_producto', item.id_producto)
    item.cantidad = data.get('cantidad', item.cantidad)
    db.session.commit()
    return carrito_schema.jsonify(item), 200

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_item_carrito(id):
    item = Carrito.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"mensaje": "Item eliminado del carrito exitosamente"}), 200
