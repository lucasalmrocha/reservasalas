from email.policy import default
from wsgiref.validate import validator
from xmlrpc.client import boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, TimeField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Optional

class ReservaForm(FlaskForm):
    sala = SelectField(u'Sala', coerce=int, validators=[DataRequired()]) #coerce faz com que o select retorne um valor especifico ao selecionar um item, no caso quero que ele retorne o id da sala escolhida
    observacoes = TextAreaField('Observações', validators=[Length(max=120)])
    data = DateField('Data', validators=[InputRequired()])
    hora_inicio = TimeField('Início', validators=[DataRequired()], format='%H:%M')
    hora_fim = TimeField('Fim', validators=[DataRequired()], format='%H:%M')
    repetir = BooleanField('Repetir toda semana', default=False)
    fim_repeticao = DateField('Repetir até', validators=[Optional()])
    submit = SubmitField('Reservar')