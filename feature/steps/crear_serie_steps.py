from behave import given, when, then
from database.models import Serie, Supervisor, Grupo, Curso
from DBManager import db
from app.services.serie_service import SerieService

@given('soy un profesor autenticado')
def step_impl(context):
    context.profesor = Supervisor(nombres="Juan", apellidos="Henderson", correo="juanH@udec.cl", password="1234")
    db.session.add(context.profesor)
    db.session.commit()

@when('ingreso el nombre "{nombre}", activo la serie y la asigno al grupo "{grupo_nombre}"')
def step_impl(context, nombre, grupo_nombre):
    context.serie_data = {
        'nombre': nombre,
        'activa': True,
        'grupo_nombre': grupo_nombre
    }

@when('presiono el botón de crear serie')
def step_impl(context):
    try:
        nueva_serie = SerieService.create_serie(
            nombre=context.serie_data['nombre'],
            activa=context.serie_data['activa'],
            grupo_nombre=context.serie_data['grupo_nombre']
        )
        context.serie_creada = nueva_serie

        context.response = {'message': "Serie creada exitosamente", 'status': 201}
        print(f"Serie creada: {context.serie_creada.nombre}")
    except Exception as e:
        context.response = {'message': f"Error al crear serie: {e}", 'status': 500}
        context.error_occurred = True
        print(f"Error al crear serie: {e}. Respuesta: {context.response}")

@then('la serie "{nombre_serie}" debe guardarse en la base de datos')
def step_impl(context, nombre_serie):
    serie = SerieService.get_serie_by_nombre(nombre_serie)
    assert serie is not None, f"La serie '{nombre_serie}' no se encontró en la base de datos."
    assert serie.activa == True, f"La serie '{nombre_serie}' no está activa."
    print(f"Verificación de guardado en DB exitosa para serie '{nombre_serie}'.")

@then('debo ver un mensaje de éxito')
def step_impl(context):
    assert hasattr(context, 'response'), "El objeto 'context.response' no está definido."
    assert context.response.get('message') == "Serie creada exitosamente", \
        f"Mensaje de éxito esperado 'Serie creada exitosamente' pero se recibió '{context.response.get('message')}'"
    print(f"Verificación de mensaje de éxito exitosa: '{context.response.get('message')}'")

@then('debo ver la serie "{nombre_serie}" en el listado')
def step_impl(context, nombre_serie):
    series = SerieService.get_all_series()
    nombres_series = [s.nombre for s in series]
    assert nombre_serie in nombres_series, f"La serie '{nombre_serie}' no se encontró en el listado de series."
    print(f"Verificación de listado de serie exitosa: '{nombre_serie}' está presente.")

@then('la serie "{nombre_serie}" debe estar asignada al grupo "{nombre_grupo}"')
def step_impl(context, nombre_serie, nombre_grupo):
    assert SerieService.is_serie_assigned_to_group(nombre_serie, nombre_grupo), \
        f"La serie '{nombre_serie}' no está asignada al grupo '{nombre_grupo}'."
    print(f"Verificación de asignación de serie a grupo exitosa: '{nombre_serie}' asignada a '{nombre_grupo}'.")

