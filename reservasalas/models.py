from datetime import datetime
from reservasalas import db, login_manager
from flask import current_app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #image_file = db.Column(db.String(20), unique=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    reservas = db.relationship('Reservas', backref='author', lazy=True)
    salas = db.relationship('Sala', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
	
class Sala(db.Model):
    __tablename__='salas'
    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(50), nullable=False)
    tipo_sala = db.Column(db.String(50), nullable=False)
    tipo_lousa = db.Column(db.String(50), nullable=False)
    tipo_piso = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.String(100), nullable=False)
    andar = db.Column(db.String(50), nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    bloco_torre = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    reservas = db.relationship('Reservas', backref='salas', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Sala('{self.sala}', '{self.date_created}')"

class Reservas(db.Model):
    __tablename__='reservas'
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reservante = db.Column(db.String(50), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.String(120))
    data_creacao = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Reservas('{self.sala_id}', '{self.user_id}', '{self.inicio}', '{self.fim}', '{self.observacoes})"