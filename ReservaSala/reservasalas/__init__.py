from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from reservasalas.utils.utility_functions import load_user

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.user_loader(load_user)
#bcrypt = Bcrypt()

def create_app(config_class=None):
    app = Flask(__name__,
            instance_relative_config=True,
            template_folder = "templates")
    app.config.from_pyfile(config_class)
    app.secret_key = '79c98fa30075e727d1857f87f5306819'
    from reservasalas.models.models import User, Sala, Reservas

    db.init_app(app)
    with app.app_context():
        db.create_all()
    #bcrypt.init_app(app)
    login_manager.init_app(app)
    
    register_blueprints(app)

    return app

def initialize_extensions(application):
    global db, login_manager
    db = SQLAlchemy(application)
            #session_options={"autoflush": False})
    login_manager = LoginManager(application) 
    login_manager.user_loader(load_user)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

def register_blueprints(app):
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