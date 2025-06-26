from flask import Blueprint, request, jsonify
from app.services.asignar_grupos import (
    asignar_estudiante_a_grupo,
    remover_estudiante_de_grupo
)

bp = Blueprint('main', __name__)

@bp.route('/asignar_grupo', methods=['POST'])
def asignar_grupo_endpoint():
    """
    Endpoint para asignar un estudiante a un grupo.
    Espera un JSON con 'matricula_estudiante', 'nombre_grupo' y 'id_curso'.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400

    matricula_estudiante = data.get('matricula_estudiante')
    nombre_grupo = data.get('nombre_grupo')
    id_curso = data.get('id_curso')

    if not all([matricula_estudiante, nombre_grupo, id_curso is not None]):
        return jsonify({"error": "Faltan campos requeridos: matricula_estudiante, nombre_grupo, id_curso"}), 400
    
    try:
        id_curso = int(id_curso)
    except ValueError:
        return jsonify({"error": "El campo 'id_curso' debe ser un número entero válido"}), 400

    estudiante_data = {"matricula": matricula_estudiante}
    grupo_data = {"nombre": nombre_grupo, "id_curso": id_curso}

    response, status_code = asignar_estudiante_a_grupo(estudiante_data, grupo_data)

    return jsonify(response), status_code


@bp.route('/remover_grupo', methods=['POST'])
def remover_grupo_endpoint():
    """
    Endpoint para remover un estudiante de un grupo.
    Espera un JSON con 'matricula_estudiante', 'nombre_grupo' y 'id_curso'.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400

    matricula_estudiante = data.get('matricula_estudiante')
    nombre_grupo = data.get('nombre_grupo')
    id_curso = data.get('id_curso')

    if not all([matricula_estudiante, nombre_grupo, id_curso is not None]):
        return jsonify({"error": "Faltan campos requeridos: matricula_estudiante, nombre_grupo, id_curso"}), 400
    
    try:
        id_curso = int(id_curso)
    except ValueError:
        return jsonify({"error": "El campo 'id_curso' debe ser un número entero válido"}), 400

    estudiante_data = {"matricula": matricula_estudiante}
    grupo_data = {"nombre": nombre_grupo, "id_curso": id_curso}

    response, status_code = remover_estudiante_de_grupo(estudiante_data, grupo_data)

    return jsonify(response), status_code