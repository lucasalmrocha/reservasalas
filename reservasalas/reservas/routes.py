from crypt import methods
from datetime import datetime, timedelta
from flask import (render_template, url_for, flash,
					redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from reservasalas import db
from reservasalas.models.models import Reservas, Sala
from reservasalas.reservas.forms import ReservaForm
from reservasalas.reservas.utils import verificaConflitoDataReservas
from flask import Blueprint
#from collections import namedtuple
from sqlalchemy import and_
from wtforms.validators import InputRequired
from reservasalas.utils.permissoes import verifica_permissao
from reservasalas.utils.utility_functions import primeira_sala

reservas = Blueprint('reservas', __name__)

@reservas.route("/reservas/nova_reserva/<int:sala_id>", methods=['GET', 'POST'])
@login_required
@verifica_permissao('cadastrar_reserva')
def nova_reserva(sala_id):
	form = ReservaForm()

	#trazendo as salas do banco de dados para o select de sala
	salas = Sala.query.order_by(Sala.sala)
	lista_salas = [(i.id, i.sala) for i in salas]
	form.sala.choices=lista_salas

	if form.repetir.data == True:
		form.fim_repeticao.validators=[InputRequired()]

	events_reservas = Reservas.query.filter(Reservas.sala_id==int(sala_id))

	if form.validate_on_submit():
		datetime_inicio = datetime.combine(form.data.data,form.hora_inicio.data)
		datetime_fim = datetime.combine(form.data.data,form.hora_fim.data)

		#trazendo a lista de reservas para verificar se há algum overlaping na hora de cadastrar reservas
		lista_reservas = Reservas.query.filter(and_(Reservas.fim>datetime.today(), Reservas.sala_id==form.sala.data))
		lista_horarios_reservas = [[inicio.inicio for inicio in lista_reservas], [fim.fim for fim in lista_reservas]]
		
		if form.hora_inicio.data>=form.hora_fim.data:
			flash('O horário final não pode ser menor ou igual ao horário inicial!')
		elif verificaConflitoDataReservas(lista_horarios_reservas, datetime_inicio, datetime_fim) == True: #verificando se há overlaping de reserva
			flash('Já existe uma reserva para esta sala neste horário!', 'warning')
		else :
			if form.repetir.data == True:
				date_fim_repeticao = form.fim_repeticao.data
				repeticoes = ((date_fim_repeticao-form.data.data).days)/7
				for i in range(0,int(repeticoes)):
					reserva = Reservas(sala_id=form.sala.data, observacoes=form.observacoes.data, reservante=current_user.username,
					inicio=datetime_inicio+timedelta(days=i * 7), fim=datetime_fim+timedelta(days=i*7), data_creacao=datetime.today(),
					sala_nome = Sala.query.get(form.sala.data).sala, author = current_user)
					db.session.add(reserva)
					db.session.commit()
				flash('Reservas cadastradas!', 'success')
			else:
				reserva = Reservas(sala_id=form.sala.data, observacoes=form.observacoes.data, reservante=current_user.username,
				inicio=datetime_inicio, fim=datetime_fim, data_creacao=datetime.today(), sala_nome=Sala.query.get(form.sala.data).sala, author = current_user)
				db.session.add(reserva)
				db.session.commit()
				flash('Reserva cadastrada!', 'success')
			return redirect(url_for('reservas.ver_reservas'))
	form.sala(autocomplete="on")

	return render_template('criar_reserva.html', title='Nova Sala', form = form, legend="Criar reserva", events=events_reservas, primeira_sala=primeira_sala())


@reservas.route("/reservas/<int:reserva_id>")
def reserva(reserva_id):
	reserva = Reservas.query.get_or_404(reserva_id)
	sala = Sala.query.get_or_404(reserva.sala_id)
	return render_template('reserva.html', reserva=reserva, sala=sala, primeira_sala=primeira_sala())

@reservas.route("/reservas/<int:reserva_id>/update", methods=['GET', 'POST'])
@login_required
@verifica_permissao('atualizar_reserva')
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
		reserva.observacoes = form.observacoes.data
		reserva.inicio = datetime.combine(form.data.data,form.hora_inicio.data)
		reserva.fim = datetime.combine(form.data.data,form.hora_fim.data)
		db.session.commit()
		flash('Reserva atualizada!', 'success')
		return redirect(url_for('reservas.reserva', reserva_id=reserva.id))
	elif request.method == 'GET':
		form.sala.data = Sala.query.get_or_404(reserva.sala_id)
		form.observacoes.data = reserva.observacoes
		form.data.data = reserva.inicio
		form.hora_inicio.data = reserva.inicio
		form.hora_fim.data = reserva.fim
	return render_template('criar_reserva.html', title='Atualizar reserva', form=form, legend="Atualizar reserva", primeira_sala=primeira_sala())

@reservas.route("/reservas/<int:reserva_id>/delete", methods=['GET', 'POST'])
@login_required
@verifica_permissao('excluir_reserva')
def delete_reserva(reserva_id):
	reserva = Reservas.query.get_or_404(reserva_id)
	if reserva.author != current_user:
		abort(403)
	db.session.delete(reserva)
	db.session.commit()
	flash('Reserva deletada!', 'success')
	return redirect(url_for('main.home'), primeira_sala=primeira_sala())

@reservas.route("/reservas/ver_reservas")
@login_required
@verifica_permissao('ver_reservas')
def ver_reservas():
	page = request.args.get('page', 1, type=int)
	#lista de reservas que estão válidas (salas reservadas para o momento atual ou posterior)
	# no momento em que o usuário está acessando o sistema
	reservas = Reservas.query.filter(Reservas.fim>=datetime.today()).order_by(Reservas.inicio).paginate(page=page, per_page=5)
	reservas_events = Reservas.query.filter(Reservas.fim>=datetime.today()).order_by(Reservas.inicio)
	salas = Sala.query.order_by(Sala.sala)
	return render_template('ver_reservas.html', reservas=reservas, salas=salas, events=reservas_events, primeira_sala=primeira_sala())