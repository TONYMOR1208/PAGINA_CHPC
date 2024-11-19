from flask import Blueprint, jsonify, request
from models import db, Categoria
from schemas.categoria_schema import CategoriaSchema
from sqlalchemy.exc import IntegrityError

categoria_bp = Blueprint('categorias', __name__)

# Helper para respuestas estándar
def create_response(data=None, message="", status="success", code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }
    return jsonify(response), code


@categoria_bp.route('/categorias', methods=['GET'])
def obtener_categorias():
    categorias = Categoria.query.all()
    categoria_schema = CategoriaSchema(many=True)
    return create_response(data=categoria_schema.dump(categorias), message="Lista de categorías obtenida")


@categoria_bp.route('/categorias/<int:id>', methods=['GET'])
def obtener_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    categoria_schema = CategoriaSchema()
    return create_response(data=categoria_schema.dump(categoria), message="Categoría obtenida")


@categoria_bp.route('/categorias', methods=['POST'])
def crear_categoria():
    data = request.get_json()
    categoria_schema = CategoriaSchema()
    errors = categoria_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    nueva_categoria = Categoria(
        nombre_categoria=data['nombre_categoria'],
        descripcion=data.get('descripcion'),
        id_categoria_padre=data.get('id_categoria_padre')
    )
    try:
        db.session.add(nueva_categoria)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad. Verifica el ID de la categoría padre.", status="error", code=400)

    return create_response(data=categoria_schema.dump(nueva_categoria), message="Categoría creada", code=201)


@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
def actualizar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    data = request.get_json()
    categoria_schema = CategoriaSchema()
    errors = categoria_schema.validate(data)
    if errors:
        return create_response(data=errors, message="Errores de validación", status="error", code=400)

    categoria.nombre_categoria = data.get('nombre_categoria', categoria.nombre_categoria)
    categoria.descripcion = data.get('descripcion', categoria.descripcion)
    categoria.id_categoria_padre = data.get('id_categoria_padre', categoria.id_categoria_padre)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return create_response(message="Error de integridad. Verifica el ID de la categoría padre.", status="error", code=400)

    return create_response(data=categoria_schema.dump(categoria), message="Categoría actualizada")


@categoria_bp.route('/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    categoria = Categoria.query.get_or_404(id)

    if categoria.subcategorias:
        return create_response(
            message="No se puede eliminar una categoría que tiene subcategorías.",
            status="error",
            code=400
        )

    db.session.delete(categoria)
    db.session.commit()
    return create_response(message="Categoría eliminada", code=204)
