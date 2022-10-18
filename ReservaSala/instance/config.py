import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost/reservasalas'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

SESSION_TYPE = "filesystem"


INIT_LDAP_TEST = True
LDAP_TEST_USERS = ["hugo", "jose", "prof1", "luiz", "aluno1", "aluno2", "orientador1", "secretaria1", "coordenador", "patinhas", "patooficial"]
LDAP_TEST_USERS += [ "marcelo.reyes", "raphael.camargo", "thiago.covoes", "e.francesquini", "folivetti",
                    "jeronimo.pellegrini", "mauricio.richartz", "vinicius.pazuch",
                    "francisco.bezerra", "saul.leite", "alejandra.rada",
                    "rodrigo.pavao", "raquel.fornari", "lucas" ]
LDAP_TEST_PASS = "teste"
LDAP_URL = "localhost"
LDAP_PORT = 8389
LDAP_QUERY = "uid={},ou=users,dc=ufabc,dc=edu,dc=br"

SMTP_EMAIL = "lucasalmrocha@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PASS = ""
SMTP_PORT = "587"

PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
SESSION_REFRESH_EACH_REQUEST = True