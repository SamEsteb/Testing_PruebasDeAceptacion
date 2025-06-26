from behave import given, when, then # type: ignore
from app.services.user_service import registro_supervisor
from database.models import Supervisor

@when('ingreso un correo electrónico único "{correo}"')
def step_impl(context, correo):
   
    context.form_data['correo'] = correo

@when('hago clic en el botón "Registrar Supervisor"')
def step_impl(context):

    supervisor = registro_supervisor(context.form_data)
    context.response = supervisor
    if supervisor:
        context.response.status_code = 201
    else:
        context.response.status_code = 400

@then("un nuevo registro de 'Supervisor' debe existir en la base de datos con el correo \"{correo}\"")
def step_impl(context, correo):
    
    # Usamos el modelo Supervisor para buscar en la BD de prueba.
    supervisor = Supervisor.query.filter_by(correo=correo).first()

    # Aserción 1: El supervisor debe haber sido creado.
    assert supervisor is not None, f"No se encontró un Supervisor con el correo {correo} en la BD."

    # Aserción 2 (Recomendada): Verificamos que los datos son correctos.
    # Usamos la clave 'nombres' que debe haber sido guardada por el step del nombre.
    assert supervisor.nombres == context.form_data['nombres']
    assert supervisor.apellidos == context.form_data['apellidos']