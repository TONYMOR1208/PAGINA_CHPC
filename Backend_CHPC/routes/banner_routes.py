from flask import Blueprint, request, jsonify
from models import Banner
from schemas.banner_schema import BannerSchema
from app import db

bp = Blueprint('banner_routes', __name__, url_prefix='/banners')

banner_schema = BannerSchema()
banners_schema = BannerSchema(many=True)

@bp.route('/', methods=['GET'])
def obtener_banners():
    banners = Banner.query.all()
    return jsonify(banners_schema.dump(banners)), 200

@bp.route('/<int:id>', methods=['GET'])
def obtener_banner(id):
    banner = Banner.query.get_or_404(id)
    return jsonify(banner_schema.dump(banner)), 200

@bp.route('/', methods=['POST'])
def crear_banner():
    data = request.get_json()
    try:
        banner = banner_schema.load(data)
        db.session.add(banner)
        db.session.commit()
        return jsonify(banner_schema.dump(banner)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_banner(id):
    banner = Banner.query.get_or_404(id)
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(banner, key, value)
        db.session.commit()
        return jsonify(banner_schema.dump(banner)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_banner(id):
    banner = Banner.query.get_or_404(id)
    try:
        db.session.delete(banner)
        db.session.commit()
        return jsonify({"message": "Banner eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
