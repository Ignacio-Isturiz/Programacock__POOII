from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración del correo
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Usa el mismo correo

    db.init_app(app)
    mail.init_app(app)  # ← ¡FUNDAMENTAL!

    # Registrar blueprints
    from src.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Redirección desde raíz hacia login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
