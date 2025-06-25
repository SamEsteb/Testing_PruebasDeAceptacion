from behave import given, when, then # type: ignore


@given('que me encuentro en la página de registro')
def step_impl(context):
    pass

@when('ingreso un nombre válido "{nombre}"')
def step_impl(context, nombre):
    pass

@when('ingreso un apellido válido "{apellidos}"')
def step_impl(context, apellidos):
    pass
@when('ingreso mi numero de matricula "{matricula}"')
def step_impl(context, matricula):
    pass

@when('ingreso un correo electrónico unico "{correo}"')
def step_impl(context, correo):
    pass

@when('ingreso una contraseña segura "{password}"')
def step_impl(context, password):
    pass

@when('ingreso una carrera válida "{carrera}"')
def step_impl(context, carrera):
    pass

@when('hago clic en el botón "Registrar Estudiante"')
def step_impl(context):
    pass

@then('soy redirigido a la página de inicio de sesión o mi sesión se inicia automáticamente')
def step_impl(context):
    pass

@then("un nuevo registro de 'Estudiante' debe existir en la base de datos con el correo \"{correo}\"")
def step_impl(context, correo):
    pass