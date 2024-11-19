from marshmallow import Schema, fields

class MediaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    tipo_media = fields.Str(required=True)
    url = fields.Str(required=True)
    descripcion = fields.Str()
    orden = fields.Int()
