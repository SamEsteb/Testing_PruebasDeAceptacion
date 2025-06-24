from app import create_app
from DBManager import db

def before_all(context):
    # Crear app y contexto para pruebas
    context.app = create_app()
    context.app_context = context.app.app_context()
    context.app_context.push()

    # Crear todas las tablas en la base de datos
    db.create_all()

def after_all(context):
    db.session.remove()
    db.drop_all() 
    context.app_context.pop()
