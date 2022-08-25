from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from reservasalas.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/reservasalas'
    app.config['SECRET_KEY'] = '79c98fa30075e727d1857f87f5306819'
    from reservasalas.models import User, Sala, Reservas

    db.init_app(app)
    with app.app_context():
        db.create_all()
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from reservasalas.main.routes import main
    from reservasalas.salas.routes import salas
    from reservasalas.users.routes import users
    from reservasalas.reservas.routes import reservas
    from reservasalas.errors.handlers import errors
    
    app.register_blueprint(main)
    app.register_blueprint(salas)
    app.register_blueprint(users)
    app.register_blueprint(reservas)
    app.register_blueprint(errors)


    return app