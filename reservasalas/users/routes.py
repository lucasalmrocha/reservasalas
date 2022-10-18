from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from reservasalas import db#, bcrypt
from reservasalas.models.models import User, Sala
from reservasalas.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from reservasalas.utils.ldap import checa_ldap
#from reservasalas.users.utils import save_picture
from reservasalas.utils.utility_functions import primeira_sala

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		#hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #criptografando a senha do usuário
		user = User(username=form.username.data, login=form.login.data)#, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('register.html', title='Register', form=form, primeira_sala=primeira_sala())

@users.route("/login", methods=['GET','POST'])
def login():
	form = LoginForm()

	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	if form.validate_on_submit():
		login = form.login.data
		senha = form.password.data

		ok = login and senha and checa_ldap(login, senha)

		if not ok:
			flash("Usário ou senha errados! Tente novamente", 'danger')
			return render_template('login.html', title='Login', form=form)
		
		user=User.query.filter_by(login=form.login.data).first()
		if user is None:
			flash('Seu usuário não está cadastrado no sistema!', 'warning')
			return render_template('login.html', title='Login', form=form)
		
		login_user(user, remember=form.remember.data)
		next_page = request.args.get('next')
		return redirect(next_page) if next_page else redirect(url_for('main.home'))

		# user=User.query.filter_by(login=form.login.data).first()
		# if user and bcrypt.check_password_hash(user.password, form.password.data):
		# 	login_user(user, remember=form.remember.data)
		# 	next_page = request.args.get('next')
		# 	return redirect(next_page) if next_page else redirect(url_for('main.home'))
		# else:
		# 	flash('Login Unsuccessful.', 'danger')
	return render_template('login.html', title='Login', form=form, primeira_sala=primeira_sala())

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		#if form.picture.data:
		#	picture_file = save_picture(form.picture.data)
		#	current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.login = form.login.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET': #condição para pegar os dados do usuário e coloca-los nos inputs
		form.username.data = current_user.username
		form.login.data = current_user.login
	#image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', 
							#image_file = image_file,
							form = form, primeira_sala=primeira_sala())

#@users.route("/user/<string:username>")
#def user_posts(username):
#	page = request.args.get('page', 1, type=int) #parâmetro de consulta de páginas. Sem ele na próxima linha, apenas seria mostrada uma única página
#	user = User.query.filter_by(username=username).first_or_404()
#	posts = Post.query.filter_by(author=user)\
#		.order_by(Post.date_posted.desc())\
#		.paginate(page=page, per_page=2) #fazendo com que não sejam mostradas todas os posts de uma única vez. Nesse caso serão mostrados apenas 5 posts
#	return render_template('user_posts.html', posts = posts, user = user)