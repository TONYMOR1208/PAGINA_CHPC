from flask import Blueprint, jsonify, request
from models import db, Carrito
from schemas.carrito_schema import CarritoSchema
from sqlalchemy.exc import IntegrityError

carrito_bp = Blueprint('carrito', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


# Obtener todos los ítems del carrito
@carrito_bp.route('/', methods=['GET'])
def obtener_carrito():
    items = Carrito.query.all()
    carrito_schema = CarritoSchema(many=True)
    return create_response(data=carrito_schema.dump(items), message="Lista de ítems del carrito obtenida")


# Obtener un ítem del carrito por ID
@carrito_bp.route('/<int:id>', methods=['GET'])
def obtener_item_carrito(id):
    item = Carrito.query.get_or_404(id)
    carrito_schema = CarritoSchema()
    return create_response(data=carrito_schema.dump(item), message="Ítem del carrito obtenido")


# Agregar un nuevo ítem al carrito
@carrito_bp.route('/', methods=['POST'])
def agregar_al_carrito():
    data = request.get_json()
    carrito_schema = CarritoSchema()
    errors = carrito_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nuevo_item = Carrito(
        id_cliente=data['id_cliente'],
        id_producto=data['id_producto'],
        cantidad=data['cantidad']
    )
    try:
        db.session.add(nuevo_item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al agregar el ítem. Verifica las claves foráneas.", status="error", code=400)

    return create_response(data=carrito_schema.dump(nuevo_item), message="Ítem agregado al carrito", code=201)


# Actualizar la cantidad de un ítem del carrito
@carrito_bp.route('/<int:id>', methods=['PUT'])
def actualizar_item_carrito(id):
    item = Carrito.query.get_or_404(id)
    data = request.get_json()
    carrito_schema = CarritoSchema()
    errors = carrito_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    item.cantidad = data.get('cantidad', item.cantidad)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al actualizar el ítem del carrito.", status="error", code=400)

    return create_response(data=carrito_schema.dump(item), message="Ítem del carrito actualizado")


# Eliminar un ítem del carrito
@carrito_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_item_carrito(id):
    item = Carrito.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return create_response(message="Ítem del carrito eliminado", code=204)
