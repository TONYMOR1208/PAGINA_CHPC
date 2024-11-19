from flask import Flask, jsonify
from config import Config
from models import db, bcrypt
from flask_jwt_extended import JWTManager
from auth.routes import auth

from flask_migrate import Migrate
from flask_cors import CORS
from marshmallow import ValidationError
import logging

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Configurar logging
logging.basicConfig(level=logging.INFO)

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

# Ruta de prueba
@app.route("/")
def index():
    return jsonify({"mensaje": "La API está funcionando correctamente"})

app.register_blueprint(auth, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
