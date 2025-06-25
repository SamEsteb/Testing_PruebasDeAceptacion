from behave import given, then
from database.models import Serie, Grupo, Curso, serie_asignada
from DBManager import db

@given('existe una serie llamada "{nombre_serie}" asignada al grupo "{nombre_grupo}"')
def step_impl(context, nombre_serie, nombre_grupo):
    """
    Precondición: Crea una serie y la asigna a un grupo para simular una serie existente.
    """
    curso = Curso.query.filter_by(nombre="Curso Base").first()
    if not curso:
        curso = Curso(nombre="Curso Base", activa=True)
        db.session.add(curso)
        db.session.commit()
        db.session.refresh(curso)

    grupo = Grupo.query.filter_by(nombre=nombre_grupo).first()
    if not grupo:
        grupo = Grupo(nombre=nombre_grupo, id_curso=curso.id)
        db.session.add(grupo)
        db.session.commit()
        db.session.refresh(grupo)

    serie = Serie.query.filter_by(nombre=nombre_serie).first()
    if not serie:
        serie = Serie(nombre=nombre_serie, activa=True)
        db.session.add(serie)
        db.session.commit()
        db.session.refresh(serie)

    assignment_exists = db.session.query(serie_asignada).filter(
        serie_asignada.c.id_serie == serie.id,
        serie_asignada.c.id_grupo == grupo.id
    ).first()
    if not assignment_exists:
        db.session.execute(serie_asignada.insert().values(id_serie=serie.id, id_grupo=grupo.id))
        db.session.commit()

    context.grupo_existente = grupo
    context.serie_preexistente = serie

@then('la serie "{nombre_serie}" no debe duplicarse en la base de datos')
def step_impl(context, nombre_serie):
    """
    Verifica que no se ha creado una nueva instancia de la serie con el nombre duplicado.
    Solo debería existir la instancia preexistente.
    """
    series = Serie.query.filter_by(nombre=nombre_serie).all()
    assert len(series) == 1, f"Se encontró {len(series)} series con nombre '{nombre_serie}', se esperaba 1."
    print(f"Verificación de duplicidad exitosa: Solo existe una serie '{nombre_serie}'.")