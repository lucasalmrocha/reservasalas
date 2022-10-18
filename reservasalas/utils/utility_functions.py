
def load_user(user_id):
    from reservasalas.models.models import User

    return User.query.get(int(user_id))

def primeira_sala():
    from reservasalas.models.models import Sala
    salas_query = Sala.query.order_by(Sala.sala)
    primeira_sala_id_select = int(salas_query.first().id if salas_query.first()!=None else -1) #variavel que irá passar a primeira sala para trazer as reservas da mesma quando estiver na página de cadastro de reservas

    return int(primeira_sala_id_select)