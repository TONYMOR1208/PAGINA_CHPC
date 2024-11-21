from flask import Blueprint, request, jsonify
from models import Reseña
from schemas.reseña_schema import ReseñaSchema
from app import db

bp = Blueprint('reseña_routes', __name__, url_prefix='/reseñas')

reseña_schema = ReseñaSchema()
reseñas_schema = ReseñaSchema(many=True)

@bp.route('/', methods=['POST'])
def crear_reseña():
    data = request.json
    errors = reseña_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    nueva_reseña = Reseña(
        id_producto=data['id_producto'],
        id_cliente=data['id_cliente'],
        calificacion=data['calificacion'],
        texto_resena=data.get('texto_resena')
    )
    db.session.add(nueva_reseña)
    db.session.commit()
    return reseña_schema.jsonify(nueva_reseña), 201

@bp.route('/', methods=['GET'])
def obtener_reseñas():
    reseñas = Reseña.query.all()
    return reseñas_schema.jsonify(reseñas), 200

@bp.route('/<int:id>', methods=['GET'])
def obtener_reseña(id):
    reseña = Reseña.query.get_or_404(id)
    return reseña_schema.jsonify(reseña), 200

@bp.route('/<int:id>', methods=['PUT'])
def actualizar_reseña(id):
    reseña = Reseña.query.get_or_404(id)
    data = request.json
    errors = reseña_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    reseña.id_producto = data.get('id_producto', reseña.id_producto)
    reseña.id_cliente = data.get('id_cliente', reseña.id_cliente)
    reseña.calificacion = data.get('calificacion', reseña.calificacion)
    reseña.texto_resena = data.get('texto_resena', reseña.texto_resena)
    db.session.commit()
    return reseña_schema.jsonify(reseña), 200

@bp.route('/<int:id>', methods=['DELETE'])
def eliminar_reseña(id):
    reseña = Reseña.query.get_or_404(id)
    db.session.delete(reseña)
    db.session.commit()
    return jsonify({"mensaje": "Reseña eliminada exitosamente"}), 200
