import os #necessário para pegar a extensão do arquivo que o usuário envio como imagem
import secrets #necessário para criar um nome aleatório para a imagem do usuário
from PIL import Image #usado para comprimir imagens
from flask import current_app

def save_picture(form_picture):
	random_hex = secrets.token_hex(8) #gerando o hex para criar o nome do arquivo a ser salvo no banco de dados
	_, f_ext = os.path.splitext(form_picture.filename) #pega o nome do arquivo que o usuário fez upload e divide em duas variáveis, uma para o nome em si e outra para a extensão do arquivo
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) #montando o caminho da imagem no banco de dados

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn