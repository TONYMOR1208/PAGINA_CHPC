from marshmallow import Schema, fields
from datetime import datetime

class BannerSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    imagen_url = fields.Str(required=True)
    texto_adicional = fields.Str(allow_none=True)
    fecha_inicio = fields.Date(allow_none=True)  # Aceptar fechas nulas
    fecha_fin = fields.Date(allow_none=True)    # Aceptar fechas nulas
    orden = fields.Int(default=0)
    estado = fields.Boolean(default=True)
    fecha_creacion = fields.DateTime(dump_only=True, default=datetime.utcnow)
    fecha_modificacion = fields.DateTime(dump_only=True, default=datetime.utcnow)
