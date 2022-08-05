from datetime import datetime
from flask_login import UserMixin
from reservasalas import db, login_manager

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=True, default='default.jpg')
    password = db.Column(db.String(60), unique=True, nullable=False)
    salas = db.relationship('Sala', backref='author', lazy=True)
    reservas = db.relationship('Reservas', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
	
class Sala(db.Model):
    __tablename__='sala'
    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(50), nullable=False)
    tipo_sala = db.Column(db.String(50), nullable=False)
    tipo_lousa = db.Column(db.String(50), nullable=False)
    tipo_piso = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.String(100), nullable=False)
    andar = db.Column(db.String(10), nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reservas = db.relationship('Reservas', backref='sala', lazy=True)

    def __repr__(self):
        return f"Sala('{self.sala}', '{self.date_created}')"

class Reservas(db.Model):
    __tablename__='reservas'
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    horario_inicial = db.Column(db.DateTime, nullable=False)
    horario_final = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Sala('{self.sala}', '{self.date_created}')"