from flask import (render_template, url_for, flash,
					redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from reservasalas import db
from reservasalas.models import Sala
from reservasalas.salas.forms import SalaForm

from flask import Blueprint

salas = Blueprint('salas', __name__)

@salas.route("/sala/new", methods=['GET', 'POST'])
@login_required
def nova_sala():
	form = SalaForm()
	if form.validate_on_submit():
		sala= Sala(title=form.title.data, content=form.content.data, author=current_user) #na modelagem do bd não há author, mas funciona no lugar do user_id que está na modelagem
		db.session.add(sala)
		db.session.commit()
		flash('Sala cadastrada!', 'success')
		return redirect(url_for('main.home'))
	return render_template('criar_sala.html', title='Nova Sala', form = form)

@salas.route("/sala/<int:sala_id>")
def sala(sala_id):
	sala = Sala.query.get_or_404(sala_id)
	return render_template('sala.html', title=sala.title, sala=sala)

@salas.route("/sala/<int:sala_id>/update", methods=['GET', 'POST'])
@login_required
def update_sala(sala_id):
	sala = Sala.query.get_or_404(sala_id)
	if sala.author != current_user:
		abort(403)
	form = SalaForm()
	if form.validate_on_submit():
		sala.title = form.title.data
		sala.content = form.content.data
		db.session.commit()
		flash('Sala atualizada!', 'success')
		return redirect(url_for('salas.sala', sala_id=sala.id))
	elif request.method == 'GET':
		form.title.data = sala.title
		form.content.data = sala.content
	return render_template('create_sala.html', title='Atualizar sala', form=form, legend="Atualizar sala")

@salas.route("/sala/<int:sala_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_sala(sala_id):
	sala = sala.query.get_or_404(sala_id)
	if sala.author != current_user:
		abort(403)
	db.session.delete(sala)
	db.session.commit()
	flash('Sala deletada!', 'success')
	return redirect(url_for('main.home'))