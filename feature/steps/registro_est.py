from behave import given, when, then # type: ignore
from database.models import Estudiante
from app.services.user_service import registro_estudiante


@given('que me encuentro en la página de registro')
def step_impl(context):
    # Creamos un diccionario para almacenar los datos del formulario
    context.form_data = {}

@when('ingreso un nombre válido "{nombre}"')
def step_impl(context, nombre):
    # Almacenamos el nombre en el diccionario del contexto
    context.form_data['nombres'] = nombre

@when('ingreso un apellido válido "{apellidos}"')
def step_impl(context, apellidos):
    # Almacenamos el apellido en el diccionario del contexto
    context.form_data['apellidos'] = apellidos

@when('ingreso mi numero de matricula "{matricula}"')
def step_impl(context, matricula):
    # Almacenamos el número de matrícula en el diccionario del contexto
    context.form_data['matricula'] = matricula

@when('ingreso un correo electrónico unico "{correo}"')
def step_impl(context, correo):
    # Almacenamos el correo electrónico en el diccionario del contexto
    context.form_data['correo'] = correo

@when('ingreso una contraseña segura "{password}"')
def step_impl(context, password):
    # Almacenamos la contraseña en el diccionario del contexto
    context.form_data['password'] = password

@when('ingreso una carrera válida "{carrera}"')
def step_impl(context, carrera):
    # Almacenamos la carrera en el diccionario del contexto
    context.form_data['carrera'] = carrera

@when('hago clic en el botón "Registrar Estudiante"')
def step_impl(context):
    estudiante = registro_estudiante(context.form_data)
    context.response = estudiante
    if estudiante:
        context.response.status_code = 201
    else:
        context.response.status_code = 400

@then('soy redirigido a la página de inicio de sesión o mi sesión se inicia automáticamente')
def step_impl(context):
    # Verificamos que la respuesta sea un redireccionamiento
    assert context.response.status_code == 201, f"Código de estado esperado 201, pero se recibió {context.response.status_code}"


@then("un nuevo registro de 'Estudiante' debe existir en la base de datos con el correo \"{correo}\"")
def step_impl(context, correo):
    # Verificamos que el estudiante se haya registrado correctamente
    #Buscamos el estudiante en la base de datos por correo
    estudiante = Estudiante.query.filter_by(correo=correo).first()
    #El estudiante no debe ser None
    assert estudiante is not None, f"No se encontró un estudiante con el correo {correo}"
    
    # Verificamos que los datos del estudiante coincidan con los del formulario
    assert estudiante.nombres == context.form_data['nombres'], "El nombre del estudiante no coincide"
    assert estudiante.apellidos == context.form_data['apellidos'], "El apellido del estudiante no coincide"
    assert estudiante.matricula == context.form_data['matricula'], "La matrícula del estudiante no coincide"
    assert estudiante.carrera == context.form_data['carrera'], "La carrera del estudiante no coincide"