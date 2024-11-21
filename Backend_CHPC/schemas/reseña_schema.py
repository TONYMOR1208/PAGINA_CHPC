from marshmallow import Schema, fields, validate

class ReseñaSchema(Schema):
    id_producto = fields.Int(
        required=True,
        error_messages={"required": "El producto es obligatorio."}
    )
    id_cliente = fields.Int(
        required=True,
        error_messages={"required": "El cliente es obligatorio."}
    )
    calificacion = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=5, error="La calificación debe estar entre 1 y 5.")
    )
    texto_resena = fields.Str(
        validate=validate.Length(max=1000, error="El texto de la reseña debe tener como máximo 1000 caracteres.")
    )
    fecha_resena = fields.DateTime(
        dump_only=True
    )
