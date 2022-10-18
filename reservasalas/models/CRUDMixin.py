"""
.. module:: CRUDMixin
   :platform: Unix, Windows
   :synopsis: Helper de CRUD para todos os modelos.

.. moduleauthor:: Emílio Francesquini

Baseado no código do Flask-Kit:
https://github.com/semirook/flask-kit/blob/master/ext.py
"""
from sqlalchemy import Column
from reservasalas import db
from datetime import datetime

class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    excluido_em = db.Column(db.DateTime)
    data_criacao =  db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.now)
    data_edicao = db.Column(db.DateTime,
                                 nullable=False, default=datetime.now,
                                 onupdate=datetime.now)

    @classmethod
    def create(cls, commit=True, **kwargs):
        """Cria um registro."""
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    @classmethod
    def get(cls, id):
        """Recupera um registro."""
        return cls.query.get(id)

    @classmethod
    def getOrCreate(cls, id):
      """Tenta recuperar um registro, se não existir, tenta criar."""
      if id is None:
        return cls()
      else:
        return cls.get(id)

    @classmethod
    def get_or_404(cls, id):
        """Recupera um registro, se não existir dá erro 404."""
        return cls.query.get_or_404(id)

    @classmethod
    def listar(cls):
        """Lista todas as entradas."""
        return cls.query.filter_by(excluido_em = None)

    def salvar(self):
        """Salva um registro."""
        db.session.add(self)
        db.session.commit()
        return self

    def remover(self):
        """Remove um registro."""
        self.excluido_em = datetime.today()
        return db.session.commit()
