from flask import Blueprint, jsonify, request
from models import db, Marca
from schemas.marca_schema import MarcaSchema
from sqlalchemy.exc import IntegrityError

marca_bp = Blueprint('marcas', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


# Obtener todas las marcas
@marca_bp.route('/marcas', methods=['GET'])
def obtener_marcas():
    marcas = Marca.query.all()
    marca_schema = MarcaSchema(many=True)
    return create_response(data=marca_schema.dump(marcas), message="Lista de marcas obtenida")


# Obtener una marca específica por ID
@marca_bp.route('/marcas/<int:id>', methods=['GET'])
def obtener_marca(id):
    marca = Marca.query.get_or_404(id)
    marca_schema = MarcaSchema()
    return create_response(data=marca_schema.dump(marca), message="Marca obtenida")


# Crear una nueva marca
@marca_bp.route('/marcas', methods=['POST'])
def crear_marca():
    data = request.get_json()
    marca_schema = MarcaSchema()
    errors = marca_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nueva_marca = Marca(
        nombre_marca=data['nombre_marca'],
        descripcion=data.get('descripcion'),
        sitio_web=data.get('sitio_web')
    )
    try:
        db.session.add(nueva_marca)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al crear la marca.", status="error", code=400)

    return create_response(data=marca_schema.dump(nueva_marca), message="Marca creada", code=201)


# Actualizar una marca existente
@marca_bp.route('/marcas/<int:id>', methods=['PUT'])
def actualizar_marca(id):
    marca = Marca.query.get_or_404(id)
    data = request.get_json()
    marca_schema = MarcaSchema()
    errors = marca_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    marca.nombre_marca = data.get('nombre_marca', marca.nombre_marca)
    marca.descripcion = data.get('descripcion', marca.descripcion)
    marca.sitio_web = data.get('sitio_web', marca.sitio_web)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad al actualizar la marca.", status="error", code=400)

    return create_response(data=marca_schema.dump(marca), message="Marca actualizada")


# Eliminar una marca
@marca_bp.route('/marcas/<int:id>', methods=['DELETE'])
def eliminar_marca(id):
    marca = Marca.query.get_or_404(id)

    if marca.productos_marca:
        return create_response(
            message="No se puede eliminar una marca que tiene productos asociados.",
            status="error",
            code=400
        )

    db.session.delete(marca)
    db.session.commit()
    return create_response(message="Marca eliminada", code=204)
