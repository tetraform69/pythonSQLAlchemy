from app import app
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models.categoria import *
from models.producto import *

from models.categoria import *
from models.producto import *

with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    producto = None
    categorias = Categoria.query.all()

    return render_template("formProducto.html", categorias=categorias, producto=producto)