import os
from flask import Flask
from dotenv import load_dotenv

from DBManager import init_app, db
from app import create_app

# Cargar variables del archivo .env
load_dotenv()

def build_app():
    app = Flask(__name__)

    # Configuración desde variables de entorno
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-por-defecto')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos y blueprints
    init_app(app)
    create_app(app)

    return app

app = build_app()

@app.route('/')
def index():
    return ":) Flask funcionando correctamente!"

if __name__ == '__main__':
    app.run(debug=True)
