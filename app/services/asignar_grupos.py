from database.models import db, Estudiante, Grupo
from sqlalchemy.exc import IntegrityError 


def asignar_estudiante_a_grupo(estudiante_data: dict, grupo_data: dict):
    """
    Intenta asignar un estudiante a un grupo existente.
    Este servicio **asume que el estudiante y el grupo YA DEBEN EXISTIR** para la asignación.
    Si no existen, retorna un error apropiado (404).
    """
    matricula_estudiante = estudiante_data.get('matricula')
    nombre_grupo = grupo_data.get('nombre')
    id_curso = grupo_data.get('id_curso')

    print(f"DEBUG: Intentando asignar estudiante '{matricula_estudiante}' al grupo '{nombre_grupo}' (Curso: {id_curso})")

    # Buscar estudiante por matrícula. Si no existe, retornar error.
    # No crear estudiante aquí, pues el escenario es para un estudiante que *no* existe.
    estudiante = verificar_existencia_estudiante(matricula_estudiante)
    if not estudiante:
        print(f"DEBUG: Estudiante con matrícula '{matricula_estudiante}' no encontrado.")
        db.session.rollback() # Limpia la sesión si hay operaciones pendientes
        return {"mensaje": f"El estudiante con matrícula '{matricula_estudiante}' no existe."}, 404

    # Buscar grupo por nombre y curso. Si no existe, retornar error.
    # No crear grupo aquí.
    grupo = verificar_existencia_grupo(nombre_grupo, id_curso)
    if not grupo:
        print(f"DEBUG: Grupo '{nombre_grupo}' para curso '{id_curso}' no encontrado.")
        db.session.rollback()
        return {"mensaje": f"El grupo '{nombre_grupo}' para el curso '{id_curso}' no existe."}, 404


    #Asignar al grupo
    try:
        grupo.estudiantes.append(estudiante)
        db.session.commit()
        print(f"DEBUG: Estudiante '{matricula_estudiante}' asignado a '{nombre_grupo}' exitosamente.")
        return {"mensaje": "Estudiante asignado correctamente"}, 200
    except IntegrityError as e:
        db.session.rollback()
        print(f"DEBUG: Error de integridad al asignar: {e}")
        return {"error": "Error de base de datos al asignar el estudiante. Podría ser una duplicidad."}, 500
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error inesperado al asignar: {e}")
        return {"error": f"Ocurrió un error inesperado: {str(e)}"}, 500

def verificar_existencia_estudiante(matricula: str) -> Estudiante | None:
    """
    Verifica si un estudiante con la matrícula dada existe en la base de datos.
    Retorna el objeto Estudiante si existe, None en caso contrario.
    """
    print(f"DEBUG: Verificando existencia de estudiante con matrícula: {matricula}")
    return Estudiante.query.filter_by(matricula=matricula).first()

def verificar_existencia_grupo(nombre_grupo: str, id_curso: int) -> Grupo | None:
    """
    Verifica si un grupo con el nombre y id_curso dados existe en la base de datos.
    Retorna el objeto Grupo si existe, None en caso contrario.
    """
    print(f"DEBUG: Verificando existencia de grupo: {nombre_grupo} (Curso: {id_curso})")
    return Grupo.query.filter_by(nombre=nombre_grupo, id_curso=id_curso).first()

def crear_estudiante_para_test(estudiante_data: dict) -> Estudiante:
    """
    Crea y guarda un estudiante en la DB si no existe.
    """
    estudiante = Estudiante.query.filter_by(matricula=estudiante_data['matricula']).first()
    if not estudiante:
        estudiante = Estudiante(
            matricula=estudiante_data['matricula'],
            nombres=estudiante_data['nombres'],
            apellidos=estudiante_data['apellidos'],
            correo=estudiante_data['correo'],
            password=estudiante_data['password'],
            carrera=estudiante_data['carrera']
        )
        db.session.add(estudiante)
        db.session.commit()
        print(f"DEBUG: Estudiante {estudiante_data['matricula']} creado para test.")
    else:
        print(f"DEBUG: Estudiante {estudiante_data['matricula']} ya existe.")
    return estudiante

def crear_grupo_para_test(grupo_data: dict) -> Grupo:
    """
    Crea y guarda un grupo en la DB si no existe.
    """
    grupo = Grupo.query.filter_by(nombre=grupo_data['nombre'], id_curso=grupo_data['id_curso']).first()
    if not grupo:
        grupo = Grupo(
            nombre=grupo_data['nombre'],
            id_curso=grupo_data['id_curso']
        )
        db.session.add(grupo)
        db.session.commit()
        print(f"DEBUG: Grupo {grupo_data['nombre']} (curso {grupo_data['id_curso']}) creado para test.")
    else:
        print(f"DEBUG: Grupo {grupo_data['nombre']} (curso {grupo_data['id_curso']}) ya existe.")
    return grupo

