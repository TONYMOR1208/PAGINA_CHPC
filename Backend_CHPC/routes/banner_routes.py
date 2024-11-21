from flask import Blueprint, request, jsonify
from models import Banner
from schemas.banner_schema import BannerSchema
from app import db

bp = Blueprint('banner_routes', __name__, url_prefix='/banners')

banner_schema = BannerSchema()
banners_schema = BannerSchema(many=True)

@bp.route('/', methods=['POST'])
def crear_banner():
    data = request.json
    errors = banner_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    nuevo_banner = Banner(
        titulo=data['titulo'],
        imagen_url=data['imagen_url'],
        texto_adicional=data.get('texto_adicional'),
        fecha_inicio=data['fecha_inicio'],
        fecha_fin=data['fecha_fin'],
        orden=data.get('orden', 0),
        estado=data.get('estado', True)
    )
    db.session.add(nuevo_banner)
    db.session.commit()
    return banner_schema.jsonify(nuevo_banner), 201

@bp.route('/', methods=['GET'])
def obtener_banners():
    banners = Banner.query.all()
    return banners_schema.jsonify(banners), 200

@bp.route('/<int:id>', methods=['GET'])
def obtener_banner(id):
    banner = Banner.query.get_or_404(id)
    return banner_schema.jsonify(banner), 200

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_banner(id):
    banner = Banner.query.get_or_404(id)
    data = request.json
    errors = banner_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    banner.titulo = data.get('titulo', banner.titulo)
    banner.imagen_url = data.get('imagen_url', banner.imagen_url)
    banner.texto_adicional = data.get('texto_adicional', banner.texto_adicional)
    banner.fecha_inicio = data.get('fecha_inicio', banner.fecha_inicio)
    banner.fecha_fin = data.get('fecha_fin', banner.fecha_fin)
    banner.orden = data.get('orden', banner.orden)
    banner.estado = data.get('estado', banner.estado)
    db.session.commit()
    return banner_schema.jsonify(banner), 200

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_banner(id):
    banner = Banner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    return jsonify({"mensaje": "Banner eliminado exitosamente"}), 200
