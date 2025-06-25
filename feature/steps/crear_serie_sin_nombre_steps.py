from behave import when, then
from app.services.serie_service import SerieService

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

@then('no debo ver la serie en el listado')
def step_impl(context):
    """
    Verifica que la serie no aparece en el listado de series.
    """
    nombre_intento = context.serie_data['nombre']
    series = SerieService.get_all_series()
    assert not any(serie.nombre == nombre_intento for serie in series), \
        f"La serie '{nombre_intento}' fue encontrada en el listado, cuando no debería."
