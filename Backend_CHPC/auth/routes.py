from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request
from datetime import timedelta
from models import db, Usuario
from auth.schemas import UsuarioSchema, LoginSchema

auth = Blueprint('auth', __name__)

@auth.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    errors = UsuarioSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    # Forzar el rol "cliente" para registros desde el frontend
    rol = data.get('rol', 'cliente')
    if rol != 'cliente':
        return jsonify({"mensaje": "No puedes asignar roles desde el registro. Rol asignado: cliente"}), 403

    nombre_usuario = data.get('nombre_usuario')
    contraseña = data.get('contraseña')
    email = data.get('email')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return jsonify({"mensaje": "El nombre de usuario ya existe"}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El correo electrónico ya existe"}), 400

    usuario = Usuario(
        nombre_usuario=nombre_usuario,
        email=email,
        telefono=telefono,
        direccion=direccion,
        rol='cliente'
    )
    usuario.set_password(contraseña)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = LoginSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nombre_usuario = data.get('nombre_usuario')
    contraseña = data.get('contraseña')

    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    if usuario and usuario.check_password(contraseña):
        access_token = create_access_token(
            identity={"id": usuario.id, "nombre_usuario": usuario.nombre_usuario, "rol": usuario.rol},
            expires_delta=timedelta(hours=1)
        )
        return jsonify(access_token=access_token), 200

    return jsonify({"mensaje": "Credenciales incorrectas"}), 401

@auth.route('/crear_admin', methods=['POST'])
def crear_admin():
    verify_jwt_in_request()
    claims = get_jwt()

    if claims.get("rol") != 'administrador':
        return jsonify({"mensaje": "No tienes permisos para crear administradores."}), 403

    data = request.get_json()
    errors = UsuarioSchema().validate(data)
    if errors:
        return jsonify(errors), 400

    nombre_usuario = data.get('nombre_usuario')
    contraseña = data.get('contraseña')
    email = data.get('email')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return jsonify({"mensaje": "El nombre de usuario ya existe"}), 400
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"mensaje": "El correo electrónico ya existe"}), 400

    admin = Usuario(
        nombre_usuario=nombre_usuario,
        email=email,
        telefono=telefono,
        direccion=direccion,
        rol='administrador'
    )
    admin.set_password(contraseña)
    db.session.add(admin)
    db.session.commit()

    return jsonify({"mensaje": "Administrador creado con éxito"}), 201
