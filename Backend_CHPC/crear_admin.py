from models import db, Usuario
from app import app  # Importa la aplicación Flask desde app.py
from datetime import datetime


def crear_admin():
    nombre_usuario = "admin"
    contraseña = "admin123$"
    email = "Anthony@admin.com"
    telefono = "04937472728"  # Teléfono predeterminado
    direccion = "Dirección predeterminada"  # Dirección predeterminada

    # Crear el administrador solo si no existe
    if not Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        admin = Usuario(
            nombre_usuario=nombre_usuario,
            email=email,
            telefono=telefono,
            direccion=direccion,
            rol='administrador',
            fecha_registro=datetime.utcnow(),
            fecha_modificacion=datetime.utcnow(),
        )
        admin.set_password(contraseña)
        db.session.add(admin)
        db.session.commit()
        print("Administrador creado con éxito.")
    else:
        print("El administrador ya existe.")

if __name__ == "__main__":
    # Iniciar el contexto de la aplicación
    with app.app_context():
        crear_admin()
