from flask import Blueprint, jsonify, request
from models import db, Banner
from schemas.banner_schema import BannerSchema
from sqlalchemy.exc import IntegrityError
from datetime import datetime

banner_bp = Blueprint('banners', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


# Obtener todos los banners
@banner_bp.route('/', methods=['GET'])
def obtener_banners():
    banners = Banner.query.all()
    banner_schema = BannerSchema(many=True)
    return create_response(data=banner_schema.dump(banners), message="Lista de banners obtenida")


# Obtener un banner específico por ID
@banner_bp.route('/<int:id>', methods=['GET'])
def obtener_banner(id):
    banner = Banner.query.get_or_404(id)
    banner_schema = BannerSchema()
    return create_response(data=banner_schema.dump(banner), message="Banner obtenido")


# Crear un nuevo banner
@banner_bp.route('/', methods=['POST'])
def crear_banner():
    data = request.get_json()
    banner_schema = BannerSchema()
    errors = banner_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nuevo_banner = Banner(
        titulo=data['titulo'],
        imagen_url=data['imagen_url'],
        texto_adicional=data.get('texto_adicional'),
        fecha_inicio=data.get('fecha_inicio'),
        fecha_fin=data.get('fecha_fin'),
        orden=data.get('orden', 0),
        estado=data.get('estado', True)
    )
    try:
        db.session.add(nuevo_banner)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al crear el banner.", status="error", code=400)

    return create_response(data=banner_schema.dump(nuevo_banner), message="Banner creado", code=201)


# Actualizar un banner existente
@banner_bp.route('/<int:id>', methods=['PUT'])
def actualizar_banner(id):
    banner = Banner.query.get_or_404(id)
    data = request.get_json()
    banner_schema = BannerSchema()
    errors = banner_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    banner.titulo = data.get('titulo', banner.titulo)
    banner.imagen_url = data.get('imagen_url', banner.imagen_url)
    banner.texto_adicional = data.get('texto_adicional', banner.texto_adicional)
    banner.fecha_inicio = data.get('fecha_inicio', banner.fecha_inicio)
    banner.fecha_fin = data.get('fecha_fin', banner.fecha_fin)
    banner.orden = data.get('orden', banner.orden)
    banner.estado = data.get('estado', banner.estado)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al actualizar el banner.", status="error", code=400)

    return create_response(data=banner_schema.dump(banner), message="Banner actualizado")


# Eliminar un banner
@banner_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_banner(id):
    banner = Banner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    return create_response(message="Banner eliminado", code=204)
