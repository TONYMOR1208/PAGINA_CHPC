from marshmallow import Schema, fields

class MarcaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_marca = fields.Str(required=True)
    descripcion = fields.Str()
    sitio_web = fields.Str()
    productos_marca = fields.Nested('ProductoSchema', many=True, exclude=('marca',))  # Para evitar recursión infinita
