from app import app, db
from models.categoria import *
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

@app.route("/formCategoria")
def formCategoria():
    categoria = None
    return render_template("formCategoria.html", categoria = categoria)


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
        categoria = None
        mensaje = str(err)
        
    return render_template("formCategoria.html", categoria = categoria, mensaje = mensaje)

@app.route("/listarCategoriasJson", methods=["get"])
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

@app.route("/addCategoriaJson", methods = ["post"])
def addCategoriaJson():
    try:
        datos = request.get_json()
        categoria = Categoria(nombreCat = datos["nombreCat"])
        db.session.add(categoria)
        db.session.commit()
        mensaje = "Categoria Agregada"
    except exc.SQLAlchemyError as err:
        db.session.rollback
        mensaje = "Error al agregar"
        
    return {"mensaje": mensaje}