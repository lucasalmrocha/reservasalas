from datetime import datetime
from flask import (render_template, url_for, flash,
					redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from reservasalas import db
from reservasalas.models import Reservas, Sala
from reservasalas.reservas.forms import ReservaForm

from flask import Blueprint

reservas = Blueprint('reservas', __name__)

@reservas.route("/reservas/new", methods=['GET', 'POST'])
@login_required
def nova_reserva():
	form = ReservaForm()
	#trazendo as salas do banco de dados para o select de sala
	salas = Sala.query.order_by(Sala.sala)
	lista_salas = [(i.id, i.sala) for i in salas]
	form.sala.choices=lista_salas
	if form.validate_on_submit():
		reserva = Reservas(sala_id=form.sala.data, reservante=form.reservante.data,
		 inicio=datetime.combine(form.data_inicio.data,form.hora_inicio.data), fim=datetime.combine(form.data_fim.data,form.hora_fim.data), author = current_user)
		db.session.add(reserva)
		db.session.commit()
		flash('Reserva cadastrada!', 'success')
		return redirect(url_for('main.home'))
	return render_template('criar_reserva.html', title='Nova Sala', form = form, legend="Criar reserva")

@reservas.route("/reservas/<int:reserva_id>")
def reserva(reserva_id):
	reserva = Reservas.query.get_or_404(reserva_id)
	sala = Sala.query.get_or_404(reserva.sala_id)
	return render_template('reserva.html', reserva=reserva, sala=sala)

@reservas.route("/reservas/<int:reserva_id>/update", methods=['GET', 'POST'])
@login_required
def update_reserva(reserva_id):
	reserva = Reservas.query.get_or_404(reserva_id)
	if reserva.author != current_user:
		abort(403)
	form = ReservaForm()
	salas = Sala.query.order_by(Sala.sala)
	lista_salas = [(i.id, i.sala) for i in salas]
	form.sala.choices=lista_salas
	if form.validate_on_submit():
		reserva.sala_id = form.sala.data
		reserva.reservante = form.reservante.data
		reserva.inicio = datetime.combine(form.data_inicio.data,form.hora_inicio.data)
		reserva.fim = datetime.combine(form.data_fim.data,form.hora_fim.data)
		db.session.commit()
		flash('Reserva atualizada!', 'success')
		return redirect(url_for('reservas.reserva', reserva_id=reserva.id))
	elif request.method == 'GET':
		form.sala.data = Sala.query.get_or_404(reserva.sala_id)
		form.reservante.data = reserva.reservante
		form.data_inicio.data = reserva.inicio
		form.hora_inicio.data = reserva.inicio
		form.data_fim.data = reserva.fim
		form.hora_fim.data = reserva.fim
	return render_template('criar_reserva.html', title='Atualizar reserva', form=form, legend="Atualizar reserva")

@reservas.route("/reservas/<int:reserva_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_reserva(reserva_id):
	reserva = Reservas.query.get_or_404(reserva_id)
	if reserva.author != current_user:
		abort(403)
	db.session.delete(reserva)
	db.session.commit()
	flash('Reserva deletada!', 'success')
	return redirect(url_for('main.home'))

@reservas.route("/reservas/ver_reservas")
def ver_reservas():
	page = request.args.get('page', 1, type=int)
	#lista de reservas que estão válidas (salas reservadas para o momento atual ou posterior)
	# no momento em que o usuário está acessando o sistema
	reservas = Reservas.query.filter(Reservas.fim>=datetime.today()).order_by(Reservas.inicio).paginate(page=page, per_page=2)
	salas = Sala.query.order_by()
	return render_template('ver_reservas.html', reservas=reservas, salas=salas)