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
