from behave import when

@when('dejo el campo de nombre vacío, activo la serie y la asigno al grupo "{grupo_nombre}"')
def step_impl(context, grupo_nombre):
    """
    Prepara los datos para intentar crear una serie con un nombre vacío.
    """
    context.serie_data = {
        'nombre': "",  # Nombre vacío
        'activa': True,
        'grupo_nombre': grupo_nombre
    }
    print(f"Datos de serie ingresados: Nombre='(vacío)', Activa=True, Grupo='{grupo_nombre}'")