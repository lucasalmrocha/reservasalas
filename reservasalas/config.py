#import os
import psycopg2

class Config:
    SECRET_KEY = '79c98fa30075e727d1857f87f5306819'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/reservasalas'
    conn_admin = psycopg2.connect(dbname="reservasalas", user="postgres", host="localhost", password="postgres")

    # Open a cursor to perform database operations
    #cur = conn_admin.cursor()

    # Execute a command: this creates a new table
    #cur.execute('DROP TABLE IF EXISTS ;')
    #cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
    #                                'title varchar (150) NOT NULL,'
    #                                'author varchar (50) NOT NULL,'
    #                                'pages_num integer NOT NULL,'
    #                                'review text,'
    #                                'date_added date DEFAULT CURRENT_TIMESTAMP);'
    #                                )
    #conn_admin.commit()

    #cur.close()
    #conn_admin.close()
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')