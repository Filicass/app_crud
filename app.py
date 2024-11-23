import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

#Carregando as variaveis do arquivo .env
load_dotenv()
#Obtendo a chave secreta do arquivo .env
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = SECRET_KEY 
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
