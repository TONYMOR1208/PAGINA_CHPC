from marshmallow import Schema, fields

class MediaSchema(Schema):
    id = fields.Int(dump_only=True)
    id_producto = fields.Int(required=True)
    tipo_media = fields.Str(required=True)
    url = fields.Str(required=True)
    descripcion = fields.Str(allow_none=True)
    orden = fields.Int(allow_none=True)

    producto = fields.Nested('ProductoSchema', exclude=('media_producto',), allow_none=True)
