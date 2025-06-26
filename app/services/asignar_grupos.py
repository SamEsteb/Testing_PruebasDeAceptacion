from database.models import db, Estudiante, Grupo
from sqlalchemy.exc import IntegrityError 


def asignar_estudiante_a_grupo(estudiante_data: dict, grupo_data: dict):
    matricula_estudiante = estudiante_data.get('matricula')
    nombre_grupo = grupo_data.get('nombre')
    id_curso = grupo_data.get('id_curso')

    print(f"DEBUG_SERVICE: Intentando asignar estudiante '{matricula_estudiante}' al grupo '{nombre_grupo}' (Curso: {id_curso})")

    estudiante = verificar_existencia_estudiante(matricula_estudiante)
    if not estudiante:
        print(f"DEBUG_SERVICE: Estudiante con matrícula '{matricula_estudiante}' no encontrado.")
        db.session.rollback()
        return {"mensaje": f"El estudiante con matrícula '{matricula_estudiante}' no existe."}, 404

    grupo = verificar_existencia_grupo(nombre_grupo, id_curso)
    if not grupo:
        print(f"DEBUG_SERVICE: Grupo '{nombre_grupo}' para curso '{id_curso}' no encontrado.")
        db.session.rollback()
        return {"mensaje": f"El grupo '{nombre_grupo}' para el curso '{id_curso}' no existe."}, 404


    db.session.refresh(estudiante) 

   
    for g in estudiante.grupos:
        if g.id_curso == grupo.id_curso:
        
            if g.id != grupo.id: 
                print(f"DEBUG_SERVICE: El estudiante '{matricula_estudiante}' ya pertenece a otro grupo ({g.nombre}) del curso {grupo.id_curso}.")
                db.session.rollback()
                return {"error": "El estudiante ya pertenece a un grupo de este curso"}, 400
            else: 
                print(f"DEBUG_SERVICE: El estudiante '{matricula_estudiante}' ya está asignado al grupo '{grupo.nombre}' ({grupo.id_curso}).")
                db.session.rollback()
                return {"mensaje": "El estudiante ya está asignado a este grupo."}, 409 # Conflicto

    
    try:
        grupo.estudiantes.append(estudiante)
        db.session.commit()
        print(f"DEBUG_SERVICE: Estudiante '{matricula_estudiante}' asignado a '{nombre_grupo}' exitosamente.")
        return {"mensaje": "Estudiante asignado correctamente"}, 200
    except IntegrityError as e:
        db.session.rollback()
        print(f"DEBUG_SERVICE: Error de integridad al asignar: {e}")
        return {"error": "Error de base de datos al asignar el estudiante. Podría ser una duplicidad."}, 500
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG_SERVICE: Error inesperado al asignar: {e}")
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

def remover_estudiante_de_grupo(estudiante_data: dict, grupo_data: dict):
    """
    Remueve un estudiante de un grupo específico.
    Retorna un mensaje de éxito si la remoción es exitosa, o un error si no se encuentra
    al estudiante/grupo o si el estudiante no pertenece al grupo.
    """
    matricula_estudiante = estudiante_data.get('matricula')
    nombre_grupo = grupo_data.get('nombre')
    id_curso = grupo_data.get('id_curso')

    print(f"DEBUG_SERVICE: Intentando remover estudiante '{matricula_estudiante}' del grupo '{nombre_grupo}' (Curso: {id_curso})")

  
    estudiante = verificar_existencia_estudiante(matricula_estudiante)
    if not estudiante:
        print(f"DEBUG_SERVICE: Estudiante con matrícula '{matricula_estudiante}' no encontrado para remoción.")
        db.session.rollback()
        return {"mensaje": f"El estudiante con matrícula '{matricula_estudiante}' no existe."}, 404

   
    grupo = verificar_existencia_grupo(nombre_grupo, id_curso)
    if not grupo:
        print(f"DEBUG_SERVICE: Grupo '{nombre_grupo}' para curso '{id_curso}' no encontrado para remoción.")
        db.session.rollback()
        return {"mensaje": f"El grupo '{nombre_grupo}' para el curso '{id_curso}' no existe."}, 404

  
    db.session.refresh(estudiante)
    if grupo not in estudiante.grupos:
        print(f"DEBUG_SERVICE: Estudiante '{matricula_estudiante}' no pertenece al grupo '{nombre_grupo}'.")
        db.session.rollback()
        return {"error": "El estudiante no pertenece a este grupo."}, 400

   
    try:
        grupo.estudiantes.remove(estudiante)
        db.session.commit()
        print(f"DEBUG_SERVICE: Estudiante '{matricula_estudiante}' removido de '{nombre_grupo}' exitosamente.")
        return {"mensaje": "Estudiante removido del grupo correctamente"}, 200
    except Exception as e:
        db.session.rollback()
        print(f"DEBUG_SERVICE: Error inesperado al remover estudiante: {e}")
        return {"error": f"Ocurrió un error inesperado al remover: {str(e)}"}, 500