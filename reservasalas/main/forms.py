from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, InputRequired, Length

class SearchForm(FlaskForm):
    searched=StringField('Searched', validators=[DataRequired()])
    submit = SubmitField('Pesquisar')