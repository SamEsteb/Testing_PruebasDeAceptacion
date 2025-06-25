from behave import given, when, then

@when('ingreso el nombre "{nombre_serie}" y activo la serie sin asignarla a ningún grupo')
def step_impl(context, nombre_serie):
    """
    Prepara los datos para intentar crear una serie sin asignación a grupo.
    """
    context.serie_data = {
        'nombre': nombre_serie,
        'activa': True,
        'grupo_nombre': None  # Sin grupo
    }
