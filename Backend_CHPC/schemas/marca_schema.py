from marshmallow import Schema, fields, validate

class MarcaSchema(Schema):
    nombre_marca = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80, error="El nombre de la marca debe tener entre 3 y 80 caracteres.")
    )
    descripcion = fields.Str(
        validate=validate.Length(max=255, error="La descripción debe tener como máximo 255 caracteres.")
    )
    sitio_web = fields.Url(
        allow_none=True,
        error_messages={"invalid": "Debe ser una URL válida."}
    )
