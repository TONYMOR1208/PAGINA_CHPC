from flask import Blueprint, jsonify, request
from models import db, Media
from schemas.media_schema import MediaSchema
from sqlalchemy.exc import IntegrityError

media_bp = Blueprint('media', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


# Obtener todos los medios
@media_bp.route('/media', methods=['GET'])
def obtener_media():
    medios = Media.query.all()
    media_schema = MediaSchema(many=True)
    return create_response(data=media_schema.dump(medios), message="Lista de medios obtenida")


# Obtener un medio específico por ID
@media_bp.route('/media/<int:id>', methods=['GET'])
def obtener_un_medio(id):
    medio = Media.query.get_or_404(id)
    media_schema = MediaSchema()
    return create_response(data=media_schema.dump(medio), message="Medio obtenido")


# Crear un nuevo medio
@media_bp.route('/media', methods=['POST'])
def crear_medio():
    data = request.get_json()
    media_schema = MediaSchema()
    errors = media_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nuevo_medio = Media(
        id_producto=data['id_producto'],
        tipo_media=data['tipo_media'],
        url=data['url'],
        descripcion=data.get('descripcion'),
        orden=data.get('orden', 0)
    )
    try:
        db.session.add(nuevo_medio)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al crear el medio. Verifica el ID del producto.", status="error", code=400)

    return create_response(data=media_schema.dump(nuevo_medio), message="Medio creado", code=201)


# Actualizar un medio existente
@media_bp.route('/media/<int:id>', methods=['PUT'])
def actualizar_medio(id):
    medio = Media.query.get_or_404(id)
    data = request.get_json()
    media_schema = MediaSchema()
    errors = media_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    medio.id_producto = data.get('id_producto', medio.id_producto)
    medio.tipo_media = data.get('tipo_media', medio.tipo_media)
    medio.url = data.get('url', medio.url)
    medio.descripcion = data.get('descripcion', medio.descripcion)
    medio.orden = data.get('orden', medio.orden)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al actualizar el medio. Verifica el ID del producto.", status="error", code=400)

    return create_response(data=media_schema.dump(medio), message="Medio actualizado")


# Eliminar un medio
@media_bp.route('/media/<int:id>', methods=['DELETE'])
def eliminar_medio(id):
    medio = Media.query.get_or_404(id)
    db.session.delete(medio)
    db.session.commit()
    return create_response(message="Medio eliminado", code=204)
