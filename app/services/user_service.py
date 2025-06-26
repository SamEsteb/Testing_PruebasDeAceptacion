from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

#Se importan los modelos necesarios que son el de Estudiante y el de Supervisor
from database.models import Estudiante,db, Supervisor
def registro_estudiante(datos_formulario):
    #Logica para crear un nuevo estudiante en la base de datos
    # 1. Validar si el correo ya existe en CUALQUIERA de las tablas de usuario
    correo_existente = Estudiante.query.filter_by(correo=datos_formulario['correo']).first() 
    
    if correo_existente:
        # Lanzamos una excepción que la capa de rutas pueda atrapar.
        # Es mejor que devolver un string o un booleano.
        raise ValueError("El correo electrónico ya está en uso.")

    # 2. Hashear la contraseña (¡nunca guardar en texto plano!)
    password_hasheada = generate_password_hash(datos_formulario['password'], method='pbkdf2:sha256')

    # 3. Crear la instancia del nuevo estudiante con los datos validados
    nuevo_estudiante = Estudiante(
        nombres=datos_formulario['nombres'],
        apellidos=datos_formulario['apellidos'],
        matricula=datos_formulario['matricula'],
        correo=datos_formulario['correo'],
        password=password_hasheada,  # Guardamos la contraseña hasheada
        carrera=datos_formulario['carrera']
    )

    # 4. Intentar guardar en la base de datos
    try:
        db.session.add(nuevo_estudiante)
        db.session.commit()
    except IntegrityError:
        # Si algo sale mal (ej. una restricción de la BD), hacemos rollback
        db.session.rollback()
        # Lanzamos otra excepción para notificar a la capa superior
        raise Exception("Error de base de datos al crear el estudiante.")

    # 5. Devolver el objeto recién creado

    return nuevo_estudiante

def registro_supervisor(datos_formulario):
    # 1. Validar si el correo ya existe en la tabla de Supervisor
    correo_existente = Supervisor.query.filter_by(correo=datos_formulario['correo']).first()
    if correo_existente:
        raise ValueError("El correo electrónico ya está en uso.")

    # 2. Hashear la contraseña
    password_hasheada = generate_password_hash(datos_formulario['password'], method='pbkdf2:sha256')

    # 3. Crear la instancia del nuevo supervisor
    nuevo_supervisor = Supervisor(
        nombres=datos_formulario['nombres'],
        apellidos=datos_formulario['apellidos'],
        correo=datos_formulario['correo'],
        password=password_hasheada
    )

    # 4. Intentar guardar en la base de datos
    try:
        db.session.add(nuevo_supervisor)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Exception("Error de base de datos al crear el supervisor.")

    # 5. Devolver el objeto recién creado
    return nuevo_supervisor