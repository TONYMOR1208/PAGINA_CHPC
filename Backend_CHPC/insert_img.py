import os
from app import app, db
from models import Banner

# Ruta donde están almacenadas las imágenes
static_folder = r'C:\Users\Contabilidad\PAGINA_CHPC\Backend_CHPC\static'

# Obtener todos los archivos de la carpeta
imagenes = os.listdir(static_folder)

# Iterar sobre las imágenes y agregarlas a la base de datos
with app.app_context():
    for imagen in imagenes:
        # Crear la URL relativa para la base de datos
        imagen_url = f"/static/{imagen}"
        
        # Crear un nuevo banner
        nuevo_banner = Banner(
            titulo=f"Banner para {imagen.split('.')[0]}",  # Título basado en el nombre del archivo
            imagen_url=imagen_url,
            orden=0,  # Puedes asignar un orden específico si lo necesitas
            estado=True
        )
        
        # Insertar en la base de datos
        db.session.add(nuevo_banner)
    
    # Confirmar los cambios
    db.session.commit()
    print(f"Se han insertado {len(imagenes)} banners en la base de datos.")
