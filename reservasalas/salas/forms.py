from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length

class SalaForm(FlaskForm):
    sala = StringField('Sala', validators=[DataRequired(), Length(min=5, max=30)])
    tipo_sala = SelectField('Tipo de sala', validators=[DataRequired()])
    tipo_lousa = SelectField('Tipo de lousa', validators=[DataRequired()])
    tipo_piso = SelectField('Tipo de piso', validators=[DataRequired()])
    capacidade = StringField('Capacidade', validators=[DataRequired(), Length(min=2, max=100)])
    andar = SelectField('Andar', validators=[DataRequired()])
    campus = SelectField('Campus', validators=[DataRequired()])
    submit = SubmitField('Cadastrar sala')

class CriarSala(FlaskForm):
    sala = SelectField('Sala', validators=[DataRequired()])
    horario_inicial = DateTimeField('Horário de início', validators=[DataRequired()])
    horario_final = DateTimeField('Horário de fim', validators=[DataRequired()])