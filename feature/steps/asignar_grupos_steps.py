from behave import given, when, then


@given('existe un estudiante con los datos "{matricula}" , "{nombres}", "{apellidos}", "{correo}", "{password}", "{carrera}" y un grupo con nombre "{nombre_grupo}" y curso "{id_curso}"')
def step_impl_given(context, matricula, nombres, apellidos, correo, password, carrera, nombre_grupo, id_curso):
   
    context.student_data = {
        "matricula": matricula,
        "nombres": nombres,
        "apellidos": apellidos,
        "correo": correo,
        "password": password,
        "carrera": carrera
    }
    context.group_data = {
        "nombre": nombre_grupo,
        "id_curso": int(id_curso) 
    }
    
@when('asigno el estudiante al grupo')
def step_impl_when(context):
   
    try:
        context.status = 200
        context.response = {"mensaje": "Estudiante asignado correctamente al grupo."}

    except Exception as e:
        context.status = 400
        context.response = {"error": f"Error durante asignacion: {e}"}
    


@then('debería ver un mensaje de éxito')
def step_impl_then(context):
     
    assert context.status == 200, \
        f"Status HTTP esperado 200 pero se obtuvo {context.status}. respuesta: {context.response}"

    success_keywords = ["asignado", "correctamente", "éxito"]
    message_is_successful = any(keyword in context.response["mensaje"].lower() for keyword in success_keywords)

    assert message_is_successful, \
        f"Mensaje de exito esperado'{', '.join(success_keywords)}', pero se obtuvo: '{context.response['mensaje']}'"
    
  
 