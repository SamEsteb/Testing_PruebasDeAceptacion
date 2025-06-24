from behave import given, when, then
from database.models import Serie, Supervisor
from DBManager import db

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
    nueva_serie = Serie(nombre=context.serie_data['nombre'], activa=context.serie_data['activa'])
    db.session.add(nueva_serie)
    db.session.commit()
    context.serie_creada = nueva_serie

@then('la serie debe guardarse en la base de datos')
def step_impl(context):
    serie = Serie.query.filter_by(nombre=context.serie_data['nombre']).first()
    assert serie is not None
    assert serie.activa == True

@then('debo ver la serie en el listado')
def step_impl(context):
    series = Serie.query.all()
    nombres_series = [s.nombre for s in series]
    assert context.serie_data['nombre'] in nombres_series
