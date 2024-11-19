from marshmallow import Schema, fields
from datetime import datetime

class ResenaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    id_cliente = fields.Int(required=True)
    calificacion = fields.Int(required=True, validate=lambda x: 1 <= x <= 5)  # Validación: calificación entre 1 y 5
    texto_resena = fields.Str()
    fecha_resena = fields.DateTime(dump_only=True, default=datetime.utcnow)  # Solo lectura
