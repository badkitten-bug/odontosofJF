def validate_required_fields(inputs):
    required_fields = ['nombres_input', 'apellidos_input', 'documento_input', 'fecha_nacimiento_picker', 'estado_input', 'grado_instruccion_input', 'afiliado_input']
    for field in required_fields:
        if not inputs[field].value:
            return False
    return True