from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def rol_requerido(*roles):
    def wrapper(fn):
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("rol")
            if user_role not in roles:
                return jsonify({"mensaje": "No tienes permiso para realizar esta acción"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
