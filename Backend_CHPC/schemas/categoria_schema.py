from marshmallow import Schema, fields

class CategoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_categoria = fields.Str(required=True)
    descripcion = fields.Str()
    id_categoria_padre = fields.Int()
    subcategorias = fields.Nested('CategoriaSchema', many=True, exclude=('subcategorias',))  # Para evitar recursión infinita
