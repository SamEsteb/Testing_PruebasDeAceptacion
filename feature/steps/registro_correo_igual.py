# Asegúrate de que estos imports estén al principio de tu archivo
from behave import given, when, then # type: ignore
import json

from werkzeug.security import generate_password_hash
from database.models import db, Estudiante, Supervisor


@given("que ya existe un '{rol}' con el correo electrónico \"{correo}\"")
def step_impl(context, rol, correo):
    """
    Paso de Preparación: Crea un usuario directamente en la base de datos
    para simular una condición preexistente.
    """
    # Hasheamos una contraseña de ejemplo para el usuario que vamos a crear.
    password_hasheada = generate_password_hash("password_existente_123", method="pbkdf2:sha256")
    
    # Creamos un Estudiante o Supervisor dependiendo de lo que pida el escenario.
    if rol.lower() == 'estudiante':
        usuario_existente = Estudiante(
            nombres="Pablo",
            apellidos="Neruda",
            matricula="1971-PN-001",
            correo=correo,
            password=password_hasheada,
            carrera="Poesía"
        )
    elif rol.lower() == 'supervisor':
        usuario_existente = Supervisor(
            nombres="Supervisor",
            apellidos="de Prueba",
            correo=correo,
            password=password_hasheada
        )
    else:
        # Si el rol no es válido, lanzamos un error.
        raise ValueError(f"El rol '{rol}' no es válido para este step.")

    # Guardamos este usuario en la base de datos de prueba y confirmamos la transacción.
    db.session.add(usuario_existente)
    db.session.commit()


@when("intento registrar un '{rol}' con el correo electrónico \"{correo}\"")
def step_impl(context, rol, correo):
    """
    Paso de Acción: Simula el intento de registro con datos que causarán un error.
    """
    # Preparamos los datos del formulario para el nuevo usuario que intentará registrarse.
    datos_formulario = {
        "nombres": "Usuario",
        "apellidos": "Repetido",
        "correo": correo,  # Usamos el correo duplicado
        "password": "PasswordValido123!"
    }

    # Determinamos a qué URL enviar la petición según el rol.
    if rol.lower() == 'supervisor':
        url_endpoint = '/registro/supervisor'
    elif rol.lower() == 'estudiante':
        url_endpoint = '/registro/estudiante'
        # Añadimos los campos extra que un estudiante necesita.
        datos_formulario['matricula'] = '000-DUP-000'
        datos_formulario['carrera'] = 'Ingeniería de Conflictos'
    else:
        raise ValueError(f"El rol '{rol}' no es válido para este step.")

    # Enviamos la petición POST al endpoint correspondiente.
    context.response = context.client.post(url_endpoint, data=datos_formulario)


@then("el sistema debe mostrar un mensaje de error indicando que el correo electrónico ya está en uso")
def step_impl(context):
    """
    Paso de Verificación 1: Comprueba la respuesta del servidor.
    """
    # 1. Verificamos el código de estado HTTP. '409 Conflict' es el código
    #    correcto para indicar que el recurso ya existe.
    assert context.response.status_code == 409, f"Código esperado 409, pero fue {context.response.status_code}"

    # 2. Verificamos el contenido del mensaje de error en el JSON de respuesta.
    response_json = context.response.get_json()
    assert 'error' in response_json, "La respuesta JSON no contiene la clave 'error'."
    assert "correo electrónico ya está en uso" in response_json['error'], f"El mensaje de error fue: '{response_json['error']}'"


@then("no se debe crear un nuevo registro de '{rol}' en la base de datos")
def step_impl(context, rol):
    """
    Paso de Verificación 2: Comprueba el estado final de la base de datos.
    """
    # Contamos cuántos registros del tipo especificado hay en la base de datos.
    if rol.lower() == 'supervisor':
        total_usuarios = Supervisor.query.count()
        # Solo debe haber 0 supervisores, ya que el 'Given' creó un estudiante.
        assert total_usuarios == 0, f"Se encontraron {total_usuarios} supervisores, se esperaba 0."

    elif rol.lower() == 'estudiante':
        total_usuarios = Estudiante.query.count()
        # Solo debe haber 1 estudiante (el que creamos en el paso 'Given').
        # Si se hubiera creado otro, el contador sería 2.
        assert total_usuarios == 1, f"Se encontraron {total_usuarios} estudiantes, se esperaba 1."