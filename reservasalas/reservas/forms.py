from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, InputRequired, Length

class ReservaForm(FlaskForm):
    sala = SelectField(u'Sala', coerce=int, validators=[DataRequired()]) #coerce faz com que o select retorne um valor especifico ao selecionar um item, no caso quero que ele retorne o id da sala escolhida
    reservante = StringField('Reservante', validators=[DataRequired(), Length(min=5, max=50)])
    data_inicio = DateField('Início', validators=[InputRequired()])
    hora_inicio = TimeField('', validators=[DataRequired()], format='%H:%M')
    data_fim = DateField('Fim', validators=[InputRequired()])
    hora_fim = TimeField('', validators=[DataRequired()], format='%H:%M')
    submit = SubmitField('Reservar')