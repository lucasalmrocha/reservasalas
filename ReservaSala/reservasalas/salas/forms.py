from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length

class SalaForm(FlaskForm):
    sala = StringField('Sala', validators=[DataRequired(), Length(min=5, max=30)])
    tipo_sala = SelectField(u'Tipo de sala', choices=['','Sala de estudos', 'Auditório'], validators=[DataRequired()])
    tipo_lousa = SelectField(u'Tipo de lousa', choices=['', 'Branca', 'Verde'], validators=[DataRequired()])
    tipo_piso = SelectField(u'Tipo de piso', choices=['', 'Plano', 'Elevado'], validators=[DataRequired()])
    capacidade = StringField('Capacidade', validators=[DataRequired(), Length(min=2, max=100)])
    andar = SelectField(u'Andar', choices=['', 'Térreo', '1º', '2º', '3º', '4º', '5º', '6º', '7º', '8º', '9º', '10º'], validators=[DataRequired()])
    campus = SelectField(u'Campus', choices=['','Santo André', 'São Bernardo do Campo'], validators=[DataRequired()])
    bloco_torre = SelectField(u'Bloco e torre', choices=['', 'Bloco A - Térreo', 'Bloco A - Embasamento (andares 1 e 2)',
     'Bloco A - Torre 1', 'Bloco A - Torre 2', 'Bloco A - Torre 3', 'Bloco B', 'Bloco Alpha 1', 'Bloco Alpha 2',
      'Bloco Beta'], validators=[DataRequired()])
    submit = SubmitField('Cadastrar sala')

#class CriarSala(FlaskForm):
#    sala = SelectField('Sala', validators=[DataRequired()])
#    horario_inicial = DateTimeField('Horário de início', validators=[DataRequired()])
#    horario_final = DateTimeField('Horário de fim', validators=[DataRequired()])