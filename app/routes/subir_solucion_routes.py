from flask import Blueprint, request, jsonify

from app.services.subir_solucion_service import subir_solucion 

subir_solucion_bp = Blueprint('subir_solucion_bp', __name__)

@subir_solucion_bp.route('/subir_solucion', methods=['POST'])
def endpoint_subir_solucion():
    """
    Endpoint para que un estudiante suba una solución a un ejercicio.
    Espera un JSON con 'matricula_estudiante', 'id_ejercicio' y 'codigo_solucion'.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400

    matricula_estudiante = data.get('matricula_estudiante')
    id_ejercicio = data.get('id_ejercicio')
    codigo_solucion = data.get('codigo_solucion')

    if not all([matricula_estudiante, id_ejercicio, codigo_solucion]):
        missing_fields = []
        if not matricula_estudiante: missing_fields.append('matricula_estudiante')
        if not id_ejercicio: missing_fields.append('id_ejercicio')
        if not codigo_solucion: missing_fields.append('codigo_solucion')
        return jsonify({"error": f"Faltan campos requeridos: {', '.join(missing_fields)}"}), 400
    

    response, status_code = subir_solucion(matricula_estudiante, id_ejercicio, codigo_solucion)

    return jsonify(response), status_code
