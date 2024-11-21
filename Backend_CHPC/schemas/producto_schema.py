from marshmallow import Schema, fields, validate

class ProductoSchema(Schema):
    nombre_producto = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80, error="El nombre del producto debe tener entre 3 y 80 caracteres.")
    )
    descripcion = fields.Str(
        validate=validate.Length(max=1000, error="La descripción debe tener como máximo 1000 caracteres.")
    )
    precio = fields.Decimal(
        required=True,
        as_string=True,
        validate=validate.Range(min=0, error="El precio debe ser mayor o igual a 0.")
    )
    stock = fields.Int(
        required=True,
        validate=validate.Range(min=0, error="El stock debe ser mayor o igual a 0.")
    )
    peso = fields.Decimal(
        required=True,
        as_string=True,
        validate=validate.Range(min=0, error="El peso debe ser mayor o igual a 0.")
    )
    color = fields.Str(
        validate=validate.Length(max=50, error="El color debe tener como máximo 50 caracteres.")
    )
    volumen = fields.Decimal(
        allow_none=True,
        as_string=True,
        validate=validate.Range(min=0, error="El volumen debe ser mayor o igual a 0.")
    )
    id_categoria = fields.Int(
        required=True,
        error_messages={"required": "La categoría es obligatoria."}
    )
    id_marca = fields.Int(
        required=True,
        error_messages={"required": "La marca es obligatoria."}
    )
