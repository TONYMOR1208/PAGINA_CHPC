from marshmallow import Schema, fields, validate

class BannerSchema(Schema):
    titulo = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=150, error="El título debe tener entre 3 y 150 caracteres.")
    )
    imagen_url = fields.Url(
        required=True,
        error_messages={"required": "La URL de la imagen es obligatoria.", "invalid": "Debe ser una URL válida."}
    )
    texto_adicional = fields.Str(
        validate=validate.Length(max=500, error="El texto adicional debe tener como máximo 500 caracteres.")
    )
    fecha_inicio = fields.Date(
        required=True,
        error_messages={"required": "La fecha de inicio es obligatoria."}
    )
    fecha_fin = fields.Date(
        required=True,
        error_messages={"required": "La fecha de fin es obligatoria."}
    )
    orden = fields.Int(
        validate=validate.Range(min=0, error="El orden debe ser mayor o igual a 0.")
    )
    estado = fields.Bool(
        required=True,
        error_messages={"required": "El estado es obligatorio."}
    )
