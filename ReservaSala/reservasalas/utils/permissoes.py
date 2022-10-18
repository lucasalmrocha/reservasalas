from flask import abort
from functools import wraps
from reservasalas.models.models import User

def verifica_permissao(perm):
    def verifica_permissao_interno (func):
        @wraps(func)
        def inner(*args, **kwargs):
            status_permissao = User.atualTemPermissao(perm)
            if status_permissao:
                return func(*args, **kwargs)
            elif status_permissao == "erro_autenticacao":
                abort(401, "Sessão expirada, refaça o login.")
            else:
                abort(403, "Você não tem direitos para fazer esta operação.")
        return inner
    return verifica_permissao_interno
