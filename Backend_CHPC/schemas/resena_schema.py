from marshmallow import Schema, fields

class ResenaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    id_cliente = fields.Int(required=True)
    calificacion = fields.Int(required=True, validate=lambda x: 1 <= x <= 5)
    texto_resena = fields.Str(allow_none=True)

    producto = fields.Nested('ProductoSchema', exclude=('reseñas_producto',), allow_none=True)
