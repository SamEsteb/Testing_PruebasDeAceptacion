from app import create_app
from DBManager import db
from database.models import Curso

def before_all(context):
    context.app = create_app()
    context.app_context = context.app.app_context()
    context.app_context.push()

def after_all(context):
    db.session.remove()
    db.drop_all() 
    context.app_context.pop()

def before_scenario(context, scenario):
    db.session.remove() 
    db.drop_all()       
    db.create_all()     
    
    dummy_curso = Curso.query.filter_by(nombre="Curso General Para Grupos").first()
    if not dummy_curso:
        dummy_curso = Curso(nombre="Curso General Para Grupos", activa=True)
        db.session.add(dummy_curso)
        db.session.commit()
        
    print(f"Base de Datos reiniciada para el escenario: {scenario.name}\n")

def after_scenario(context, scenario):
    db.session.remove()
    print(f"Escenario terminado: {scenario.name}\n")