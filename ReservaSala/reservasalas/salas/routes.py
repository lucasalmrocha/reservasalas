from datetime import datetime
from flask import (render_template, url_for, flash,
					redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from reservasalas import db
from reservasalas.models.models import Reservas, Sala
from reservasalas.salas.forms import SalaForm
from reservasalas.utils.utility_functions import primeira_sala
from reservasalas.utils.permissoes import verifica_permissao

from flask import Blueprint

salas = Blueprint('salas', __name__)

@salas.route("/sala/new", methods=['GET', 'POST'])
@login_required
@verifica_permissao('cadastrar_sala')
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
	salas_query = Sala.query.order_by(Sala.sala)
	primeira_sala_id_select = int(salas_query.first().id if salas_query!=None else -1)
	return render_template('criar_sala.html', title='Nova Sala', form = form, legend="Criar sala", primeira_sala=primeira_sala())

@salas.route("/sala/<int:sala_id>")
def sala(sala_id):
	reservas = Reservas.query.filter(Reservas.sala_id==sala_id and Reservas.fim>=datetime.today())
	reservas2=reservas.filter(Reservas.fim>=datetime.today())
	sala = Sala.query.get_or_404(sala_id)
	salas_query = Sala.query.order_by(Sala.sala)
	primeira_sala_id_select = int(salas_query.first().id if salas_query!=None else -1)
	return render_template('sala.html', sala=sala, reservas=reservas2,primeira_sala=primeira_sala())

@salas.route("/sala/<int:sala_id>/update", methods=['GET', 'POST'])
@login_required
@verifica_permissao('atualizar_sala')
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
	return render_template('criar_sala.html', title='Atualizar sala', form=form, legend="Atualizar sala", primeira_sala=primeira_sala())

@salas.route("/sala/<int:sala_id>/delete", methods=['GET', 'POST'])
@login_required
@verifica_permissao('deletar_sala')
def delete_sala(sala_id):
	sala = Sala.query.get_or_404(sala_id)
	if sala.author != current_user:
		abort(403)
	db.session.delete(sala)
	db.session.commit()
	flash('Sala deletada!', 'success')
	return redirect(url_for('main.home'), primeira_sala=primeira_sala())