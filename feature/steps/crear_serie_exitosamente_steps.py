from behave import then
from app.services.serie_service import SerieService

@then('la serie "{nombre_serie}" debe guardarse en la base de datos')
def step_impl(context, nombre_serie):
    """
    Verifica que la serie con el nombre especificado existe en la base de datos y está activa.
    """
    serie = SerieService.get_serie_by_nombre(nombre_serie)
    assert serie is not None, f"La serie '{nombre_serie}' no se encontró en la base de datos."
    assert serie.activa == True, f"La serie '{nombre_serie}' no está activa."
    print(f"Verificación de guardado en DB exitosa para serie '{nombre_serie}'.")

@then('debo ver la serie "{nombre_serie}" en el listado')
def step_impl(context, nombre_serie):
    """
    Verifica que la serie recién creada aparece en el listado de todas las series.
    """
    series = SerieService.get_all_series()
    nombres_series = [s.nombre for s in series]
    assert nombre_serie in nombres_series, f"La serie '{nombre_serie}' no se encontró en el listado de series."
    print(f"Verificación de listado de serie exitosa: '{nombre_serie}' está presente.")

@then('la serie "{nombre_serie}" debe estar asignada al grupo "{nombre_grupo}"')
def step_impl(context, nombre_serie, nombre_grupo):
    """
    Verifica que la serie especificada está correctamente asignada al grupo.
    """
    assert SerieService.is_serie_assigned_to_group(nombre_serie, nombre_grupo), \
        f"La serie '{nombre_serie}' no está asignada al grupo '{nombre_grupo}'."
    print(f"Verificación de asignación de serie a grupo exitosa: '{nombre_serie}' asignada a '{nombre_grupo}'.")