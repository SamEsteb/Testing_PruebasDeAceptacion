import os
from flask import Flask
from dotenv import load_dotenv
from DBManager import init_app, db
from app.routes.serie_routes import serie_bp

load_dotenv()

def create_app():
    """
    Función de fábrica para crear la instancia de la aplicación Flask.
    """
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-por-defecto')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///instance/database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_app(app)

    app.register_blueprint(serie_bp)

    return app

