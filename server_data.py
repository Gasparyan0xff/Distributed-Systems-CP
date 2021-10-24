from flask import Flask
from flask_restful import Api
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy


db_user = 'postgres'
db_pass = ''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{}:{}@localhost/TaskerDataBase'.format(db_user, db_pass)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DBTasker = SQLAlchemy(app)
CORS(app)
api = Api(app)