from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models import Banner
from schemas.banner_schema import BannerSchema
from app import db

bp = Blueprint('banner_routes', __name__, url_prefix='/banners')

banner_schema = BannerSchema()
banners_schema = BannerSchema(many=True)

@bp.route('/', methods=['GET'])
def obtener_banners():
    banners = Banner.query.order_by(Banner.orden).all()  # Ordenados por el campo `orden`
    return jsonify({"data": banners_schema.dump(banners)}), 200  # Envolver en una clave `data`

@bp.route('/<int:id>', methods=['GET'])
def obtener_banner(id):
    banner = Banner.query.get_or_404(id)
    return jsonify(banner_schema.dump(banner)), 200

@bp.route('/', methods=['POST'])
def crear_banner():
    data = request.get_json()
    try:
        banner_data = banner_schema.load(data)  # Validación con Marshmallow
        banner = Banner(**banner_data)
        db.session.add(banner)
        db.session.commit()
        return jsonify(banner_schema.dump(banner)), 201
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_banner(id):
    banner = Banner.query.get_or_404(id)
    data = request.get_json()
    try:
        banner_data = banner_schema.load(data, partial=True)  # Permitir actualizaciones parciales
        for key, value in banner_data.items():
            setattr(banner, key, value)
        db.session.commit()
        return jsonify(banner_schema.dump(banner)), 200
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_banner(id):
    banner = Banner.query.get_or_404(id)
    try:
        db.session.delete(banner)
        db.session.commit()
        return jsonify({"message": "Banner eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
