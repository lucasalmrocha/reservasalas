from datetime import datetime
from flask import (render_template, url_for, flash,
					redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from reservasalas import db
from reservasalas.models import Reservas, Sala
from reservasalas.salas.forms import SalaForm

from flask import Blueprint

salas = Blueprint('salas', __name__)

@salas.route("/sala/new", methods=['GET', 'POST'])
@login_required
def nova_sala():
	form = SalaForm()
	if form.validate_on_submit():
		sala= Sala(sala=form.sala.data, tipo_sala=form.tipo_sala.data,
					 tipo_lousa=form.tipo_lousa.data, tipo_piso=form.tipo_piso.data,
					  capacidade=form.capacidade.data, andar=form.andar.data, campus=form.campus.data,
					   bloco_torre=form.bloco_torre.data, author=current_user)
		db.session.add(sala)
		db.session.commit()
		flash('Sala cadastrada!', 'success')
		return redirect(url_for('main.home'))
	return render_template('criar_sala.html', title='Nova Sala', form = form, legend="Criar sala")

@salas.route("/sala/<int:sala_id>")
def sala(sala_id):
	reservas = Reservas.query.filter(Reservas.sala_id==sala_id and Reservas.fim>=datetime.today())
	reservas2=reservas.filter(Reservas.fim>=datetime.today())
	sala = Sala.query.get_or_404(sala_id)
	return render_template('sala.html', sala=sala, reservas=reservas2)

@salas.route("/sala/<int:sala_id>/update", methods=['GET', 'POST'])
@login_required
def update_sala(sala_id):
	sala = Sala.query.get_or_404(sala_id)
	if sala.author != current_user:
		abort(403)
	form = SalaForm()
	if form.validate_on_submit():
		sala.sala = form.sala.data
		sala.tipo_sala = form.tipo_sala.data
		sala.tipo_lousa = form.tipo_lousa.data
		sala.tipo_piso = form.tipo_piso.data
		sala.capacidade = form.capacidade.data
		sala.andar = form.andar.data
		sala.campus = form.campus.data
		sala.bloco_torre = form.bloco_torre.data
		db.session.commit()
		flash('Sala atualizada!', 'success')
		return redirect(url_for('salas.sala', sala_id=sala.id))
	elif request.method == 'GET':
		form.sala.data = sala.sala
		form.tipo_sala.data = sala.tipo_sala
		form.tipo_lousa.data = sala.tipo_lousa
		form.tipo_piso.data = sala.tipo_piso
		form.capacidade.data = sala.capacidade
		form.andar.data = sala.andar
		form.campus.data = sala.campus
		form.bloco_torre.data = sala.bloco_torre
	return render_template('criar_sala.html', title='Atualizar sala', form=form, legend="Atualizar sala")

@salas.route("/sala/<int:sala_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_sala(sala_id):
	sala = Sala.query.get_or_404(sala_id)
	if sala.author != current_user:
		abort(403)
	db.session.delete(sala)
	db.session.commit()
	flash('Sala deletada!', 'success')
	return redirect(url_for('main.home'))