from flask import Blueprint, jsonify, request
from models import db, Reseña
from schemas.resena_schema import ResenaSchema
from sqlalchemy.exc import IntegrityError

resena_bp = Blueprint('resenas', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


# Obtener todas las reseñas
@resena_bp.route('/', methods=['GET'])
def obtener_resenas():
    resenas = Reseña.query.all()
    resena_schema = ResenaSchema(many=True)
    return create_response(data=resena_schema.dump(resenas), message="Lista de reseñas obtenida")


# Obtener una reseña específica por ID
@resena_bp.route('/<int:id>', methods=['GET'])
def obtener_resena(id):
    resena = Reseña.query.get_or_404(id)
    resena_schema = ResenaSchema()
    return create_response(data=resena_schema.dump(resena), message="Reseña obtenida")


# Crear una nueva reseña
@resena_bp.route('/', methods=['POST'])
def crear_resena():
    data = request.get_json()
    resena_schema = ResenaSchema()
    errors = resena_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nueva_resena = Reseña(
        id_producto=data['id_producto'],
        id_cliente=data['id_cliente'],
        calificacion=data['calificacion'],
        texto_resena=data.get('texto_resena')
    )
    try:
        db.session.add(nueva_resena)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al crear la reseña. Verifica las claves foráneas.", status="error", code=400)

    return create_response(data=resena_schema.dump(nueva_resena), message="Reseña creada", code=201)


# Actualizar una reseña existente
@resena_bp.route('/<int:id>', methods=['PUT'])
def actualizar_resena(id):
    resena = Reseña.query.get_or_404(id)
    data = request.get_json()
    resena_schema = ResenaSchema()
    errors = resena_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    resena.id_producto = data.get('id_producto', resena.id_producto)
    resena.id_cliente = data.get('id_cliente', resena.id_cliente)
    resena.calificacion = data.get('calificacion', resena.calificacion)
    resena.texto_resena = data.get('texto_resena', resena.texto_resena)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al actualizar la reseña. Verifica las claves foráneas.", status="error", code=400)

    return create_response(data=resena_schema.dump(resena), message="Reseña actualizada")


# Eliminar una reseña
@resena_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_resena(id):
    resena = Reseña.query.get_or_404(id)
    db.session.delete(resena)
    db.session.commit()
    return create_response(message="Reseña eliminada", code=204)
