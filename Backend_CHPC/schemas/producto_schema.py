from marshmallow import Schema, fields

class ProductoSchema(Schema):
    id = fields.Int(dump_only=True)
    nombre_producto = fields.Str(required=True)
    descripcion = fields.Str(allow_none=True)
    precio = fields.Float(required=True)
    stock = fields.Int(required=True)
    peso = fields.Float(required=True)
    color = fields.Str(allow_none=True)
    volumen = fields.Float(allow_none=True)
    id_categoria = fields.Int(required=True)
    id_marca = fields.Int(required=True)

    media_producto = fields.Nested('MediaSchema', many=True, exclude=('producto',))
    reseñas_producto = fields.Nested('ReseñaSchema', many=True, exclude=('producto',))
    carrito_producto = fields.Nested('CarritoSchema', many=True, exclude=('producto',))
