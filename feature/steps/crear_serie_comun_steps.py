from behave import given, when, then
from database.models import Supervisor
from DBManager import db
from app.services.serie_service import SerieService 

@given('soy un profesor autenticado')
def step_impl(context):
    """
    Crea un profesor autenticado
    """
    context.profesor = Supervisor(nombres="Juan", apellidos="Pérez", correo="profesor_comun@ejemplo.com", password="1234")
    db.session.add(context.profesor)
    db.session.commit()

@when('ingreso el nombre "{nombre}", activo la serie y la asigno al grupo "{grupo_nombre}"')
def step_impl(context, nombre, grupo_nombre):
    """
    Prepara los datos de la serie a crear, incluyendo su nombre, estado y grupo de asignación.
    """
    context.serie_data = {
        'nombre': nombre,
        'activa': True,
        'grupo_nombre': grupo_nombre
    }

@when('presiono el botón de crear serie')
def step_impl(context):
    """
    Simula la acción de presionar el botón de crear serie.
    """
    from app.services.serie_service import SerieService
    try:
        nueva_serie = SerieService.create_serie(
            nombre=context.serie_data['nombre'],
            activa=context.serie_data['activa'],
            grupo_nombre=context.serie_data.get('grupo_nombre')
        )
        context.serie_creada = nueva_serie
        context.response = {'message': "Serie creada exitosamente", 'status': 201}
        context.error_occurred = False
    except ValueError as e:
        db.session.rollback()
        context.response = {'message': str(e), 'status': 400} 
        context.error_occurred = True
        print(f"Error al intentar crear serie: {e}. Respuesta: {context.response}")
    except Exception as e:
        db.session.rollback()
        context.response = {'message': f"Error inesperado al crear serie: {e}", 'status': 500}
        context.error_occurred = True
        print(f"Error inesperado al crear serie: {e}. Respuesta: {context.response}")

@then('la serie no debe guardarse en la base de datos')
def step_impl(context):
    """
    Verifica que la serie que se intentó crear no existe en la base de datos.
    """
    nombre_intento = context.serie_data['nombre']
    serie = SerieService.get_serie_by_nombre(nombre_intento)
    assert serie is None, f"La serie '{nombre_intento}' fue encontrada en la base de datos, cuando no debería."
    print(f"Verificación: La serie '{nombre_intento}' no se guardó en la DB.")

@then('debo ver un mensaje de éxito')
def step_impl(context):
    """
    Verifica que la respuesta del sistema contiene un mensaje de éxito.
    """
    assert hasattr(context, 'response'), "El objeto 'context.response' no está definido."
    assert not context.error_occurred, f"Se esperaba éxito, pero ocurrió un error: {context.response.get('message')}"
    assert context.response.get('message') == "Serie creada exitosamente", \
        f"Mensaje de éxito esperado 'Serie creada exitosamente' pero se recibió '{context.response.get('message')}'"
    print(f"Verificación de mensaje de éxito exitosa: '{context.response.get('message')}'")

@then('debo ver un mensaje de error indicando "{mensaje_error}"')
def step_impl(context, mensaje_error):
    """
    Verifica que la respuesta del sistema contiene un mensaje de error específico.
    """
    assert hasattr(context, 'response'), "El objeto 'context.response' no está definido."
    assert context.error_occurred, "Se esperaba un error, pero la operación fue exitosa."
    assert context.response.get('message') == mensaje_error, \
        f"Mensaje de error esperado: '{mensaje_error}', pero se recibió: '{context.response.get('message')}'"
    print(f"Verificación de mensaje de error exitosa: '{context.response.get('message')}'")