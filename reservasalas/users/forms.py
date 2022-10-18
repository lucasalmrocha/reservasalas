from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user
from reservasalas.models.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	login = StringField('Login',
		validators=[DataRequired()])
	# password = PasswordField('Password', validators=[DataRequired()])
	# confirm_password = PasswordField('Confirm password', 
	# 	validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	# def validate_username(self,username):
	# 	user = User.query.filter_by(username=username.data).first()
	# 	if user:
	# 		raise ValidationError('That username is taken. Please choose a different one!')
	
	# def validate_email(self,email):
	# 	user = User.query.filter_by (email=email.data).first()
	# 	if user:
	# 		raise ValidationError('That email is taken. Please choose a different one!')


class LoginForm(FlaskForm):
	login = StringField('login',
		validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	login = StringField('login',
		validators=[DataRequired()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	# def validate_username(self,username):
	# 	if username.data != current_user.username:
	# 		user = User.query.filter_by(username=username.data).first()
	# 		if user:
	# 			raise ValidationError('That username is taken. Please choose a different one!')
	
	# def validate_email(self,email):
	# 	if email.data != current_user.email:
	# 		user = User.query.filter_by (email=email.data).first()
	# 		if user:
	# 			raise ValidationError('That email is taken. Please choose a different one!')
