from behave import given, when, then # type: ignore
from database.models import Estudiante

# --- Implementación para el nuevo escenario ---

@when('ingreso una contraseña "{contrasena}"')
def step_impl(context, contrasena):
    """
    Este step es para manejar específicamente el campo de la contraseña en este escenario.
    Aunque la implementación es simple, tener un texto distinto a "contraseña segura"
    nos da flexibilidad.
    """
    context.form_data['password'] = contrasena


@then('el sistema debe mostrar un mensaje de error indicando que la contraseña no cumple con los requisitos de seguridad')
def step_impl(context):
    """
    Paso de Verificación 1: Comprueba la respuesta del servidor para el error de validación.
    """
    # 1. El código de estado HTTP correcto para un error de validación de datos
    # enviados por el cliente es '400 Bad Request'.
    assert context.response.status_code == 400, f"Código esperado 400, pero fue {context.response.status_code}"

    # 2. Verificamos que el JSON de respuesta contiene un mensaje de error relevante.
    response_json = context.response.get_json()
    assert 'error' in response_json, "La respuesta JSON no contiene la clave 'error'."
    
    # Comprobamos de forma flexible que el mensaje hable sobre la contraseña y los requisitos.
    # Usamos .lower() para que la comprobación no distinga mayúsculas/minúsculas.
    error_message = response_json['error'].lower()
    assert "contraseña" in error_message or "password" in error_message, f"El mensaje de error no menciona la contraseña: '{response_json['error']}'"
    assert "requisitos" in error_message or "seguridad" in error_message, f"El mensaje de error no menciona los requisitos: '{response_json['error']}'"
