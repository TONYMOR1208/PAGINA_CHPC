from marshmallow import Schema, fields

class MarcaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_marca = fields.Str(required=True)
    descripcion = fields.Str(allow_none=True)
    sitio_web = fields.Str(allow_none=True)
    productos_marca = fields.Nested('ProductoSchema', many=True, exclude=('marca',), allow_none=True)
