from flask import Flask, jsonify
from config import Config
from models import db, bcrypt
from flask_jwt_extended import JWTManager
from auth.routes import auth as auth_bp
from routes.banner_routes import bp as banner_bp
from routes.carrito_routes import bp as carrito_bp
from routes.categoria_routes import bp as categoria_bp
from routes.marca_routes import bp as marca_bp
from routes.media_routes import bp as media_bp
from routes.producto_routes import bp as producto_bp
from routes.reseña_routes import bp as resena_bp
from routes.upload_routes import upload_bp  # Nuevo: Rutas para cargar imágenes

from flask_migrate import Migrate
from flask_cors import CORS
from marshmallow import ValidationError
import logging
import os

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Configuración de carpeta para imágenes
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Habilitar CORS
CORS(app)

# Inicializar extensiones
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Manejo de errores de validación
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({
        "status": "error",
        "message": "Errores de validación",
        "errors": error.messages
    }), 400

# Ruta de prueba
@app.route("/")
def index():
    return jsonify({"mensaje": "La API está funcionando correctamente"})

# Registrar blueprints con prefijo común "/tienda"
app.register_blueprint(auth_bp, url_prefix="/tienda/auth")
app.register_blueprint(banner_bp, url_prefix="/tienda/banners")
app.register_blueprint(carrito_bp, url_prefix="/tienda/carritos")
app.register_blueprint(categoria_bp, url_prefix="/tienda/categorias")
app.register_blueprint(marca_bp, url_prefix="/tienda/marcas")
app.register_blueprint(media_bp, url_prefix="/tienda/media")
app.register_blueprint(producto_bp, url_prefix="/tienda/productos")
app.register_blueprint(resena_bp, url_prefix="/tienda/resenas")
app.register_blueprint(upload_bp, url_prefix="/tienda/uploads")  # Nuevo: Cargar imágenes

# Ejecutar aplicación
if __name__ == "__main__":
    # Crear la carpeta para subir imágenes si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
