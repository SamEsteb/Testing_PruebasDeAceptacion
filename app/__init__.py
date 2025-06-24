import os
from flask import Flask
from dotenv import load_dotenv
from DBManager import init_app

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuración desde variables de entorno
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-por-defecto')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos y registrar blueprints
    init_app(app)

    return app
