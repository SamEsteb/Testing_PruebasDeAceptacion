from database.models import db, Estudiante, Grupo

def asignar_estudiante_a_grupo(estudiante_data, grupo_data):
    # Buscar o crear estudiante
    estudiante = Estudiante.query.get(estudiante_data.get('id'))
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
        db.session.commit()  # Para obtener el id

    # Buscar o crear grupo
    grupo = Grupo.query.get(grupo_data.get('id'))
    if not grupo:
        grupo = Grupo(
            nombre=grupo_data['nombre'],
            id_curso=grupo_data['id_curso']
        )
        db.session.add(grupo)
        db.session.commit()  # Para obtener el id

    # Verifica si el estudiante ya está en un grupo del mismo curso
    for g in estudiante.grupos:
        if g.id_curso == grupo.id_curso:
            return {"error": "El estudiante ya pertenece a un grupo de este curso"}, 400

    # Asignar al grupo
    grupo.estudiantes.append(estudiante)
    db.session.commit()
    return {"mensaje": "Estudiante asignado correctamente"}, 200

