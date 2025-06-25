from behave import given, when, then
from app.services.asignar_grupos import (
    asignar_estudiante_a_grupo,
    remover_estudiante_de_grupo, 
    crear_estudiante_para_test,
    crear_grupo_para_test
)
from database.models import db


@given('existe un estudiante "{matricula}" asignado al grupo "{nombre_grupo}" del curso "{id_curso}"')
def step_impl_given_estudiante_asignado_a_grupo(context, matricula, nombre_grupo, id_curso):
    """
    Prepara el escenario asegurándose de que un estudiante ya esté asignado a un grupo.
    Reutiliza la lógica de creación y asignación.
    """
    context.estudiante_data = {
        "matricula": matricula,
        "nombres": "Estudiante Remoción",
        "apellidos": "Test",
        "correo": f"{matricula.lower()}_remove@email.com",
        "password": "pass",
        "carrera": "Ingenieria"
    }
    context.grupo_data = {
        "nombre": nombre_grupo,
        "id_curso": int(id_curso)
    }
    
    # Crea el estudiante y el grupo en la DB
    crear_estudiante_para_test(context.estudiante_data)
    crear_grupo_para_test(context.grupo_data)
    
   
    response, status = asignar_estudiante_a_grupo(context.estudiante_data, context.grupo_data)
    assert status == 200, f"Setup Failed: Could not assign student for removal test. Status: {status}, Response: {response}"
    print(f"DEBUG - Given: Estudiante '{matricula}' asignado a '{nombre_grupo}' ({id_curso}) para test de remoción.")


@when('remuevo al estudiante "{matricula}" del grupo "{nombre_grupo}" del curso "{id_curso}"')
def step_impl_when_remuevo_estudiante_de_grupo(context, matricula, nombre_grupo, id_curso):

    context.estudiante_data_remocion = { "matricula": matricula }
    context.grupo_data_remocion = { "nombre": nombre_grupo, "id_curso": int(id_curso) }

    context.response, context.status = remover_estudiante_de_grupo(
        context.estudiante_data_remocion,
        context.grupo_data_remocion
    )
    print(f"DEBUG - When: Intento de remoción - Status: {context.status}, Response: {context.response}")


@then('debería ver un mensaje de éxito por remoción')
def step_impl_then_mensaje_exito_remocion(context):
   
    assert context.status == 200, f"Expected status 200 for removal, but got {context.status}. Response: {context.response}"
    assert "mensaje" in context.response, f"Expected 'mensaje' key in response, but got: {context.response}"
    
    expected_success_keywords = ["removido", "correctamente"]
    message_is_successful = any(keyword in context.response["mensaje"].lower() for keyword in expected_success_keywords)
    
    assert message_is_successful, f"Expected success message for removal, but got: '{context.response['mensaje']}'"
    print(f"DEBUG - Then: Mensaje de éxito por remoción verificado: '{context.response['mensaje']}'")