from crypt import methods
from datetime import datetime
from flask import render_template, request, Blueprint
from reservasalas.models import Reservas, Sala
from reservasalas.main.forms import SearchForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type=int) #parâmetro de consulta de páginas. Sem ele na próxima linha, apenas seria mostrada uma única página
	salas = Sala.query.order_by(Sala.sala.desc()).paginate(page=page, per_page=2) #fazendo com que não sejam mostradas todas as salas de uma única vez. Nesse caso serão mostrados apenas 5 posts
	reservas = Reservas.query.order_by()
	events_reservas = Reservas.query.order_by()
	return render_template('home.html', salas=salas, reservas=reservas, date=datetime.today(), events=events_reservas)#, verif=0)

@main.route("/about")
def about():
	return render_template('about.html', title='About')

@main.route("/home_calendar/<int:sala_id>")
def home_calendar(sala_id):
	page = request.args.get('page', 1, type=int) #parâmetro de consulta de páginas. Sem ele na próxima linha, apenas seria mostrada uma única página
	salas = Sala.query.order_by(Sala.sala.desc()).paginate(page=page, per_page=2) #fazendo com que não sejam mostradas todas as salas de uma única vez. Nesse caso serão mostrados apenas 5 posts
	reservas = Reservas.query.order_by()
	if sala_id:
		sala = Sala.query.get_or_404(sala_id)
		reservasCalendar = Reservas.query.filter(Reservas.sala_id==sala.id)

	return render_template('home.html', salas=salas, reservas=reservas, date=datetime.today(), events=reservasCalendar)#, verif=0)

"""@main.context_processor
def layout():
	form = SearchForm()
	return dict(form=form)

@main.route("/search", methods=["POST"])
def search():
	form = SearchForm()
	searched = form.searched.data
	if form.validate_on_submit():
		return render_template("search.html", form=form, searched=searched)"""