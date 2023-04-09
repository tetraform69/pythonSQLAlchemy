from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

conexion = "mysql+pymysql://root@localhost/shop"
app.config["SQLALCHEMY_DATABASE_URI"]= conexion
app.config["UPLOAD_FOLDER"] = './static/img'

db = SQLAlchemy(app)

from controllers.inicioController import *
from controllers.productoController import *
from controllers.categoriaController import *

if __name__ == "__main__":
    app.run(port="4141", debug=True)