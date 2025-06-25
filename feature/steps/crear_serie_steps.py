from behave import given, when, then
from database.models import Serie, Supervisor
from DBManager import db
from app.services.serie_service import SerieService

@given('soy un profesor autenticado')
def step_impl(context):
    context.profesor = Supervisor(nombres="Juan", apellidos="Henderson", correo="juanH@udec.cl", password="1234")
    db.session.add(context.profesor)
    db.session.commit()

@when('ingreso el nombre "{nombre}" y activo la serie')
def step_impl(context, nombre):
    context.serie_data = {
        'nombre': nombre,
        'activa': True
    }

@when('presiono el botón de crear serie')
def step_impl(context):
    try:
        nueva_serie = SerieService.create_serie(
            nombre=context.serie_data['nombre'],
            activa=context.serie_data['activa'],
        )
        context.serie_creada = nueva_serie

        # Simular respuesta de confirmación
        context.response = {'message': "Serie creada exitosamente", 'status': 201}
        print(f"Serie creada: {context.serie_creada.nombre}")
    except Exception as e:
        context.response = {'message': f"Error al crear serie: {e}", 'status': 500}
        context.error_occurred = True
        print(f"Error al crear serie: {e}. Respuesta: {context.response}")

@then('la serie debe guardarse en la base de datos')
def step_impl(context):
    serie = SerieService.get_serie_by_nombre(context.serie_data['nombre'])
    assert serie is not None
    assert serie.activa == True

@then('debo ver un mensaje de éxito')
def step_impl(context):
    assert hasattr(context, 'response'), "El objeto 'context.response' no está definido."
    assert context.response.get('message') == "Serie creada exitosamente", \
        f"Mensaje de éxito esperado 'Serie creada exitosamente' pero se recibió '{context.response.get('message')}'"
    print(f"Verificación de mensaje de éxito exitosa: '{context.response.get('message')}'")

@then('debo ver la serie en el listado')
def step_impl(context):
    series = SerieService.get_all_series()
    nombres_series = [s.nombre for s in series]
    assert context.serie_data['nombre'] in nombres_series


