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
    nueva_serie = SerieService.create_serie(
        nombre=context.serie_data['nombre'],
        activa=context.serie_data['activa'],
        profesor_id=context.profesor.id
    )
    context.serie_creada = nueva_serie

@then('la serie debe guardarse en la base de datos')
def step_impl(context):
    serie = SerieService.get_serie_by_nombre(context.serie_data['nombre'])
    assert serie is not None
    assert serie.activa == True

@then('debo ver la serie en el listado')
def step_impl(context):
    series = SerieService.get_all_series()
    nombres_series = [s.nombre for s in series]
    assert context.serie_data['nombre'] in nombres_series
