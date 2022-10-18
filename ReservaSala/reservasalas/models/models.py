from datetime import datetime
from reservasalas import db, login_manager
from flask import current_app
from flask_login import UserMixin, current_user
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
#from reservasalas.models.CRUDMixin import CRUDMixin
import itertools
from functools import lru_cache


# @login_manager.user_loader
# def load_user(user_id):
# 	return User.query.get(int(user_id))

assoc_permissao_permissao = db.Table('permissao_permissao',
    db.Column('permissao_id', db.Integer, db.ForeignKey('permissao.id'), index=True),
    db.Column('permissao_impl_id', db.Integer, db.ForeignKey('permissao.id')),
    UniqueConstraint('permissao_id', 'permissao_impl_id', name='Permissoes implicadas únicas')
)

assoc_usuario_permissoes = db.Table('usuario_permissao',
   db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
   db.Column('permissao_id', db.Integer, db.ForeignKey('permissao.id'), primary_key=True)
)

class Permissao(db.Model):
    __tablename__ =  'permissao'
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), unique=True, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)

    implicadas = relationship("Permissao",
                                secondary=assoc_permissao_permissao,
                                primaryjoin=id==assoc_permissao_permissao.c.permissao_id,
                                secondaryjoin=id==assoc_permissao_permissao.c.permissao_impl_id)
    
    # Backref fields
    # - usuarios

    @classmethod
    def dadoNome(cls, n):
        return cls.query.filter_by(nome=n).first()

    @classmethod
    def permissaoAdminNome(cls):
        return "Administrador"

    @classmethod
    def permissaoAdmin(cls):
        return cls.dadoNome(cls.permissaoAdminNome())

    @classmethod
    def criaPermissoes(cls, perms):
        ret = []
        for n, d, ims in perms:
            imss = [cls.dadoNome(i) for i in ims]
            p = Permissao(nome=n, descricao=d, implicadas=imss)
            p.salvar()
            ret.append(p)
        return ret

    @classmethod
    def instalaPermissoesBase(cls):
        perms = [
            (cls.permissaoAdminNome(), "Todas as ações (administrador)", []),
            ("PermissaoDesignar", "Designar permissões", [])
        ]
        cls.criaPermissoes(perms)

    @classmethod
    def instala(cls):
        cls.instalaPermissoesBase()

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    login = db.Column(db.String(120), unique=True, nullable=False)
    #password = db.Column(db.String(60), nullable=False)
    reservas = db.relationship('Reservas', backref='author', lazy=True)
    salas = db.relationship('Sala', backref='author', lazy=True)
    permissoes=relationship("Permissao", secondary=assoc_usuario_permissoes)

    def __repr__(self):
        return f"User('{self.username}', '{self.login}')"
    
    @classmethod
    def atual(cls):
        if current_user.is_authenticated:
            return current_user
        else:
            return None

    @classmethod
    def atualTemPermissao(cls, perm):
        usr = cls.atual()
        if usr is None:
            return "erro_autenticacao"
        return usr.temPermissao(perm)

    @classmethod
    def atualTemAoMenosUmaPermissao(cls, perms):
        usr = cls.atual()
        return usr is not None and usr.temAoMenosUmaPermissao(perms)

    @lru_cache(maxsize=32)
    def isAdmin(self):
        return Permissao.permissaoAdmin() in self.getPermissoes()

    @lru_cache(maxsize=32)
    def getPermissoes(self):
        perms = self.permissoes
        impls = list(itertools.chain(*[p.implicadas for p in perms]))
        return set(perms).union(set(impls))

    def temPermissao (self, perm):
        return self.isAdmin() or Permissao.dadoNome(perm) in self.getPermissoes()

    def temAoMenosUmaPermissao(self, perms):
        for p in perms:
            if self.temPermissao(p):
                return True
        return False
	
class Sala(db.Model):
    __tablename__='salas'
    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(50), nullable=False)
    tipo_sala = db.Column(db.String(50), nullable=False)
    tipo_lousa = db.Column(db.String(50), nullable=False)
    tipo_piso = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.String(100), nullable=False)
    andar = db.Column(db.String(50), nullable=False)
    campus = db.Column(db.String(50), nullable=False)
    bloco_torre = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    reservas = db.relationship('Reservas', backref='salas', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Sala('{self.sala}', '{self.date_created}')"

class Reservas(db.Model):
    __tablename__='reservas'
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reservante = db.Column(db.String(50), nullable=False)
    inicio = db.Column(db.DateTime, nullable=False)
    fim = db.Column(db.DateTime, nullable=False)
    observacoes = db.Column(db.String(120))
    data_creacao = db.Column(db.DateTime, nullable=False)
    sala_nome = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Reservas('{self.sala_id}', '{self.user_id}', '{self.inicio}', '{self.fim}', '{self.observacoes})"

def instala():
    Permissao.instala()