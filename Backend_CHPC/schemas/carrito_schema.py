from marshmallow import Schema, fields
from datetime import datetime

class CarritoSchema(Schema):
    id = fields.Int(dump_only=True)
    id_cliente = fields.Int(required=True)
    id_producto = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=lambda x: x > 0)  # Validación: cantidad mayor a 0
    fecha_agregado = fields.DateTime(dump_only=True, default=datetime.utcnow)  # Solo lectura
