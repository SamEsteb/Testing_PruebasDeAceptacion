

from behave import given, when, then
from app.services.asignar_grupos import (
   
    crear_estudiante_para_test,
    crear_grupo_para_test,
    remover_estudiante_de_grupo 
)
from database.models import db 



@given('existe un estudiante "{matricula}" y un grupo "{nombre_grupo}" del curso "{id_curso}"')
def step_impl_given_estudiante_y_grupo_existen_sin_asignacion(context, matricula, nombre_grupo, id_curso):
    """
    Crea un estudiante y un grupo en la DB, pero NO los asigna entre sí.
    """
    context.estudiante_data = {
        "matricula": matricula,
        "nombres": "Estudiante No Miembro",
        "apellidos": "Test",
        "correo": f"{matricula.lower()}_nomember@email.com",
        "password": "pass",
        "carrera": "Ciencias"
    }
    context.grupo_data = {
        "nombre": nombre_grupo,
        "id_curso": int(id_curso)
    }
    
 
    crear_estudiante_para_test(context.estudiante_data)
    crear_grupo_para_test(context.grupo_data)
    print(f"DEBUG - Given: Estudiante '{matricula}' y Grupo '{nombre_grupo}' ({id_curso}) creados, sin asignación.")


@when('intento remover al estudiante "{matricula}" del grupo "{nombre_grupo}" del curso "{id_curso}"')
def step_impl_when_intento_remover_sin_pertenecer(context, matricula, nombre_grupo, id_curso):
    """
    Llama a la función de servicio para intentar remover un estudiante que no pertenece al grupo.
    """

    context.estudiante_data_remocion = { "matricula": matricula }
    context.grupo_data_remocion = { "nombre": nombre_grupo, "id_curso": int(id_curso) }

    context.response, context.status = remover_estudiante_de_grupo(
        context.estudiante_data_remocion,
        context.grupo_data_remocion
    )
    print(f"DEBUG - When: Intento de remoción de no miembro - Status: {context.status}, Response: {context.response}")


@then('debería ver un mensaje de error "{mensaje_error_esperado}"')
def step_impl_then_mensaje_error_generico(context, mensaje_error_esperado):
    """
    Verifica que el servicio devuelva un código de estado y mensaje de error específico.
    Este paso es reutilizable para varios escenarios de error.
    """
  
    assert context.status == 400, f"Expected status 400, but got {context.status}. Response: {context.response}"
    
    assert "error" in context.response or "mensaje" in context.response, \
        f"Expected 'error' or 'mensaje' key in response, but got: {context.response}"
    
   
    actual_message = context.response.get("error", context.response.get("mensaje", "")).strip()

    assert actual_message == mensaje_error_esperado, \
        f"Expected error message '{mensaje_error_esperado}', but got: '{actual_message}'"
    print(f"DEBUG - Then: Mensaje de error '{mensaje_error_esperado}' verificado.")