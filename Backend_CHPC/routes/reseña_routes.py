from flask import Blueprint, request, jsonify
from models import Reseña
from schemas.reseña_schema import ReseñaSchema
from app import db

bp = Blueprint('reseña_routes', __name__, url_prefix='/reseñas')

reseña_schema = ReseñaSchema()
reseñas_schema = ReseñaSchema(many=True)

@bp.route('/', methods=['GET'])
def obtener_reseñas():
    reseñas = Reseña.query.all()
    return jsonify(reseñas_schema.dump(reseñas)), 200

@bp.route('/<int:id>', methods=['GET'])
def obtener_reseña(id):
    reseña = Reseña.query.get_or_404(id)
    return jsonify(reseña_schema.dump(reseña)), 200
