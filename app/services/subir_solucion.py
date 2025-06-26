
mock_db_service = {
    "estudiantes": {
        "A001": {"matricula": "A001", "nombre": "Estudiante Uno De Servicio"},
        "A002": {"matricula": "A002", "nombre": "Estudiante Dos De Servicio"}
    },
    "ejercicios": {
        "E001": {"id": "E001", "descripcion": "Ejercicio de prueba de Servicio"}
    },
    "soluciones": [] 
}

def subir_solucion(matricula_estudiante: str, id_ejercicio: str, codigo_solucion: str):
    """
    Servicio para subir una solución de un estudiante para un ejercicio.
    Por ahora, simula la verificación y el guardado.
    """
    print(f"SERVICE_DEBUG: Intentando subir solución para estudiante '{matricula_estudiante}', ejercicio '{id_ejercicio}'")

    if matricula_estudiante not in mock_db_service["estudiantes"]:
        print(f"SERVICE_DEBUG: Estudiante '{matricula_estudiante}' no encontrado.")
        return {"error": f"El estudiante con matrícula '{matricula_estudiante}' no existe."}, 404

    if id_ejercicio not in mock_db_service["ejercicios"]:
        print(f"SERVICE_DEBUG: Ejercicio '{id_ejercicio}' no encontrado.")

        return {"error": "El ejercicio no existe"}, 404

    mock_db_service["soluciones"].append({
        "matricula_estudiante": matricula_estudiante,
        "id_ejercicio": id_ejercicio,
        "codigo_solucion": codigo_solucion,
        "estado": "subida" 
    })
    
    print(f"SERVICE_DEBUG: Solución para ejercicio '{id_ejercicio}' por '{matricula_estudiante}' subida exitosamente.")
 
    return {"mensaje": "Solución subida correctamente"}, 200



def subir_solucion_mock(matricula_estudiante: str, id_ejercicio: str, codigo_solucion: str, db_context: dict):
    """
    Mock de la función de servicio para ser usada en los steps de Behave.
    Usa un contexto de base de datos (db_context) pasado como argumento.
    """
    if matricula_estudiante not in db_context["estudiantes"]:
        return {"error": f"El estudiante con matrícula '{matricula_estudiante}' no existe."}, 404

    if id_ejercicio not in db_context["ejercicios"]:
        return {"error": "El ejercicio no existe"}, 404 

    db_context["soluciones"].append({
        "matricula_estudiante": matricula_estudiante,
        "id_ejercicio": id_ejercicio,
        "codigo_solucion": codigo_solucion
    })
    return {"mensaje": "Solución subida correctamente"}, 200 
