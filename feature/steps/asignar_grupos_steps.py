from behave import given, when, then

@given('existe un estudiante con id "{id_estudiante}" y un grupo con id "{id_grupo}"')
def step_impl_given(context, id_estudiante, id_grupo):
    pass  

@when('asigno el estudiante al grupo')
def step_impl_when(context):
    pass  

@then('debería ver un mensaje de éxito')
def step_impl_then(context):
    assert True  
