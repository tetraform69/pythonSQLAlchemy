from app import app, db
from models.categoria import *
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

@app.route("/formCategoria")
def formCategoria():
    categoria = None
    return render_template("formCategoria.html", categoria = categoria)

@app.route("/listarCategorias")
def listarCategorias():
    
    categorias = Categoria.query.all()
    
    json = []
    
    for c in categorias:
        categoria = {
            "idCat": c.idCat,
            "nombreCat": c.nombreCat
        }
        json.append(categoria)
    
    return json

@app.route("/addCategoria", methods=["post"])
def addCategoria():
    try:
        nombre = request.form["nombre"].upper()
        categoria = Categoria(nombreCat=nombre)
        db.session.add(categoria)
        db.session.commit()
        mensaje = "Categoria Agregada"
        
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        mensaje = str(err)
        
    return render_template("formCategoria", mensaje = mensaje)

