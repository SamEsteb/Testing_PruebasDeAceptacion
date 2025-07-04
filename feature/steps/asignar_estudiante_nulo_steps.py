from behave import given, when, then
from app.services.asignar_grupos import asignar_estudiante_a_grupo, verificar_existencia_grupo, verificar_existencia_estudiante

@given('existe un grupo con nombre "{nombre_grupo}" y curso "{id_curso}"')
def step_impl_given_grupo_existe(context, nombre_grupo, id_curso):
    """
    Este paso solo crea un grupo para el contexto, sin un estudiante.
    En una implementación real, podrías llamar a un servicio para crear
    el grupo en la base de datos o verificar su existencia.
    """
    context.grupo_data = {
        "nombre": nombre_grupo,
        "id_curso": int(id_curso)
    }

    print(f"DEBUG: 'Given' step - Grupo '{nombre_grupo}' ({id_curso}) preparado.")


@when('intento asignar al estudiante "{matricula}" al grupo')
def step_impl_when_asignar_estudiante_inexistente(context, matricula):
    """
    Intenta llamar al servicio de asignación con un estudiante que no existe.
    En una implementación real, el servicio debería retornar un error.
    """
    context.estudiante_data = {
        "matricula": matricula,
        "nombres": "Estudiante", # Datos de relleno para la prueba
        "apellidos": "Inexistente",
        "correo": "inexistente@example.com",
        "password": "pass",
        "carrera": "Carrera"
    }

    context.response, context.status = asignar_estudiante_a_grupo(context.estudiante_data, context.grupo_data)
    print(f"DEBUG: 'When' step - Intento de asignación para estudiante inexistente '{matricula}' - Status: {context.status}, Response: {context.response}")


@then('debería ver un mensaje de error indicando que el estudiante no existe')
def step_impl_then_mensaje_error(context):
    """
    Verifica que la asignación falló y que la respuesta contiene un mensaje de error
    claro para el usuario.
    """
   
    assert context.status != 200, f"Expected non-200 status, but got {context.status}. Response: {context.response}"

   
    assert "mensaje" in context.response or "error" in context.response, \
        f"Expected 'mensaje' or 'error' key in response, but got: {context.response}"

    error_message_found = False
    error_keywords = ["no existe", "estudiante no encontrado", "no se encontró el estudiante"]
    
   
    message = context.response.get("mensaje", context.response.get("error", "")).lower()

    for keyword in error_keywords:
        if keyword in message:
            error_message_found = True
            break
            
    assert error_message_found, f"Expected error message containing '{', '.join(error_keywords)}', but got: '{message}'"
    print(f"DEBUG: 'Then' step - Mensaje de error verificado: '{message}'")