from flask import render_template, request, Blueprint
from reservasalas.models import Sala

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type=int) #parâmetro de consulta de páginas. Sem ele na próxima linha, apenas seria mostrada uma única página
	salas = Sala.query.order_by(Sala.date_created.desc()).paginate(page=page, per_page=2) #fazendo com que não sejam mostradas todas os posts de uma única vez. Nesse caso serão mostrados apenas 5 posts
	return render_template('home.html', salas = salas)

@main.route("/about")
def about():
	return render_template('about.html', title='About')