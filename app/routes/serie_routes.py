from flask import Blueprint, request, jsonify
from app.services.serie_service import SerieService

serie_bp = Blueprint('series', __name__)

@serie_bp.route('/crear_serie', methods=['POST'])
def create_serie():
    """
    Ruta para crear una nueva serie.
    Espera un JSON con 'nombre', 'activa' y 'grupo_nombre'.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    activa = data.get('activa', True) 
    grupo_nombre = data.get('grupo_nombre')

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es requerido."}), 400
    if not grupo_nombre:
        return jsonify({"error": "El campo 'grupo_nombre' es requerido."}), 400

    try:
        new_serie = SerieService.create_serie(nombre, activa, grupo_nombre)
        return jsonify({
            "message": "Serie creada y asignada exitosamente",
            "serie": {
                "id": new_serie.id,
                "nombre": new_serie.nombre,
                "activa": new_serie.activa
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@serie_bp.route('/series', methods=['GET'])
def get_all_series():
    """
    Ruta para obtener todas las series.
    Retorna un JSON con la lista de series.
    """
    try:
        series = SerieService.get_all_series()
        return jsonify([{
            "id": serie.id,
            "nombre": serie.nombre,
            "activa": serie.activa
        } for serie in series]), 200
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

@serie_bp.route('/series/<int:serie_id>', methods=['GET'])
def get_serie(serie_id):
    """
    Ruta para obtener una serie específica por su ID.
    Retorna un JSON con los detalles de la serie.
    """
    try:
        if not serie_id or serie_id <= 0:
            return jsonify({"error": "ID de serie inválido"}), 400
        
        serie = SerieService.get_serie_by_id(serie_id)
        if not serie:
            return jsonify({"error": "Serie no encontrada"}), 404
        return jsonify({
            "id": serie.id,
            "nombre": serie.nombre,
            "activa": serie.activa
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500