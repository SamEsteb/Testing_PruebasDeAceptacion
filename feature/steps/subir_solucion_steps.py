from behave import given, when, then
from app.services.serie_service import SerieService
from database.models import Estudiante, Serie, Ejercicio, Grupo 
from DBManager import db
import os # Para manejo de paths de archivos dummy



@given('que existe una serie de ejercicios "{nombre_serie}" con un ejercicio "{nombre_ejercicio}"')
def step_impl_existe_serie_con_ejercicio(context, nombre_serie, nombre_ejercicio):

    test_student = Estudiante.query.filter_by(matricula="test001").first()
    if not test_student:
        test_student = Estudiante(
            matricula="test001",
            nombres="Test",
            apellidos="Student",
            correo="test.student@example.com",
            password="password",
            carrera="Ing. de Software"
        )
        db.session.add(test_student)
        db.session.commit()
    context.student_id = test_student.id


    nombre_grupo_prueba = "Grupo de Prueba para Series"
    grupo_prueba = Grupo.query.filter_by(nombre=nombre_grupo_prueba).first()
    if not grupo_prueba:

        from database.models import Curso 
        curso_general = Curso.query.filter_by(nombre="Curso General Para Grupos").first()
        if not curso_general: 
            curso_general = Curso(nombre="Curso General Para Grupos", activa=True)
            db.session.add(curso_general)
            db.session.commit()

        grupo_prueba = Grupo(nombre=nombre_grupo_prueba, id_curso=curso_general.id)
        db.session.add(grupo_prueba)
        db.session.commit()

    # Crear la serie y asignarla al grupo
    serie = SerieService.get_serie_by_nombre(nombre_serie)
    if not serie:
        # Si create_serie espera un nombre de grupo, se lo pasamos
        serie = SerieService.create_serie(nombre=nombre_serie, activa=True, grupo_nombre=nombre_grupo_prueba)
    context.serie_id = serie.id

    # Crear el ejercicio asociado a la serie
    ejercicio = Ejercicio.query.filter_by(nombre=nombre_ejercicio, id_serie=serie.id).first()
    if not ejercicio:
        ejercicio = Ejercicio(
            nombre=nombre_ejercicio,
            path_ejercicio=f"path/to/{nombre_ejercicio}.pdf", # Path dummy
            enunciado=f"Enunciado del ejercicio {nombre_ejercicio}",
            id_serie=serie.id
        )
        db.session.add(ejercicio)
        db.session.commit()
    context.ejercicio_id = ejercicio.id
    context.nombre_serie_global = nombre_serie 
    context.nombre_ejercicio_global = nombre_ejercicio 

    print(f"PASO: Dado que existe la serie '{nombre_serie}' (ID: {context.serie_id}) con el ejercicio '{nombre_ejercicio}' (ID: {context.ejercicio_id}) y estudiante (ID: {context.student_id})")

@when('un estudiante sube la solución "{nombre_solucion}" para el ejercicio "{nombre_ejercicio}" de la serie "{nombre_serie}"')
def step_impl_subir_solucion(context, nombre_solucion, nombre_ejercicio, nombre_serie):

    assert nombre_serie == context.nombre_serie_global, f"Discrepancia en nombre de serie: esperado '{context.nombre_serie_global}', obtenido '{nombre_serie}'"
    assert nombre_ejercicio == context.nombre_ejercicio_global, f"Discrepancia en nombre de ejercicio: esperado '{context.nombre_ejercicio_global}', obtenido '{nombre_ejercicio}'"


    dummy_solution_path = f"uploads/soluciones_test/{nombre_solucion}"
  
    os.makedirs(os.path.dirname(dummy_solution_path), exist_ok=True)
    with open(dummy_solution_path, "w") as f:
        f.write("Contenido dummy de la solución.")

    context.nombre_solucion_subida = nombre_solucion

    try:
        SerieService.subir_solucion_ejercicio(
            id_estudiante=context.student_id,
            id_serie=context.serie_id,
            id_ejercicio=context.ejercicio_id,
            path_solucion=dummy_solution_path, 
            nombre_archivo=nombre_solucion
        )
        context.subida_exitosa = True
        print(f"PASO: Cuando el estudiante (ID: {context.student_id}) sube la solución '{nombre_solucion}' para el ejercicio '{nombre_ejercicio}' de la serie '{nombre_serie}'")
    except Exception as e:
        context.subida_exitosa = False
        context.error_subida = str(e)
        print(f"ERROR en PASO When: {e}")
        raise e 


@then('la solución "{nombre_solucion}" queda registrada para el ejercicio "{nombre_ejercicio}" de la serie "{nombre_serie}"')
def step_impl_verificar_solucion_registrada(context, nombre_solucion, nombre_ejercicio, nombre_serie):
    assert getattr(context, 'subida_exitosa', False), f"La subida de la solución falló o no se ejecutó. Error: {getattr(context, 'error_subida', 'No hay error registrado.')}"
    assert nombre_solucion == context.nombre_solucion_subida, "El nombre del archivo de solución en el step 'then' no coincide con el subido."

    registrada = SerieService.verificar_solucion_registrada(
        id_estudiante=context.student_id,
        id_serie=context.serie_id,
        id_ejercicio=context.ejercicio_id,
        nombre_archivo=nombre_solucion
    )

    if registrada:
        print(f"PASO: Entonces la solución '{nombre_solucion}' está registrada para el ejercicio '{nombre_ejercicio}' de la serie '{nombre_serie}'. Verificación exitosa.")
    else:
        print(f"FALLO PASO Then: La solución '{nombre_solucion}' NO está registrada para el ejercicio ID {context.ejercicio_id} (Estudiante ID: {context.student_id}).")

    assert registrada, f"La solución '{nombre_solucion}' no quedó registrada para el ejercicio '{nombre_ejercicio}' (ID: {context.ejercicio_id}) de la serie '{nombre_serie}' (ID: {context.serie_id}) para el estudiante (ID: {context.student_id})."
