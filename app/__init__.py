import os
from flask import Flask
from dotenv import load_dotenv
from DBManager import init_app
from app.routes import asignar_grupo_routes

load_dotenv()

def create_app():
    app = Flask(__name__)

   
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-por-defecto')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    init_app(app)

   
    from . import routes 
    app.register_blueprint(asignar_grupo_routes.bp) 

    return app