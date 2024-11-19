from marshmallow import Schema, fields

class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_categoria = fields.Str(required=True)
    descripcion = fields.Str(allow_none=True)
    id_categoria_padre = fields.Int(allow_none=True)
    subcategorias = fields.Nested('CategoriaSchema', many=True, exclude=('subcategorias',), allow_none=True)
