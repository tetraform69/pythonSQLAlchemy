from app import app, db
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from models.producto import *
from models.categoria import *
import os


@app.route("/listarProductos")
def listarProductos():
    try:
        productos = Producto.query.all()
        mensaje = "lista de productos"
    except exc.SQLAlchemyError as ex:
        mensaje = str(ex)

    return render_template("listProducts.html", productos=productos, mensaje=mensaje)


@app.route("/formProducto")
def formProducto():
    producto = None
    categorias = Categoria.query.all()

    return render_template("formProducto.html", categorias=categorias, producto=producto)


@app.route("/addProducto", methods=["post"])
def agregarProducto():
    try:
        codigo = int(request.form["codigo"])
        nombre = request.form["nombre"]
        precio = int(request.form["precio"])
        categoria = request.form["categoria"]

        producto = Producto(codigoPro=codigo, nombrePro=nombre,
                            precioPro=precio, categoriaPro=categoria)

        db.session.add(producto)
        db.session.commit()

        foto = request.files["foto"]
        if (foto.filename != ""):
            nameFile = str(producto.idPro) + ".jpg"
            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nameFile))

        mensaje = "Producto agregado"

        return redirect("/listarProductos")

    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje = str(ex)

    categorias = Categoria.query.all()

    return render_template("formProducto.html", producto=producto, mensaje=mensaje, categorias=categorias)


@app.route("/consultarProducto/<int:idProducto>")
def consultarProducto(idProducto):
    try:
        producto = Producto.query.get(idProducto)
        categorias = Categoria.query.all()

    except exc.SQLAlchemyError as ex:
        mensaje = str(ex)

    return render_template("formEditarProducto.html", producto=producto, categorias=categorias)


@app.route("/actualizarProducto", methods=["post"])
def actualizarProducto():
    try:

        idPro = int(request.form["idPro"])
        producto = Producto.query.get(idPro)

        producto.codigoPro = request.form["codigo"]
        producto.nombrePro = request.form["nombre"]
        producto.precioPro = request.form["precio"]
        producto.categoriaPro = request.form["categoria"]

        db.session.commit()

        return redirect("/listarProductos")

    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje = str(ex)


@app.route("/eliminar/<int:idProducto>", methods=["get"])
def eliminar(idProducto):
    try:
        producto = Producto.query.get(idProducto)

        db.session.delete(producto)
        db.session.commit()

        mensaje = "Producto Eliminado"

        return redirect("/listarProductos")
    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje = str(ex)

    productos = Producto.query.all()
    return render_template("/listarProductos", productos=productos, mensaje=mensaje)


@app.route("/listarProductosJson", methods=["get"])
def listarProductosJson():
    try:
        productos = Producto.query.all()
        listJson = []

        for p in productos:
            producto = {
                "idPro": p.idPro,
                "nombrePro": p.nombrePro,
                "precioPro": p.precioPro,
                "categoria": {
                    "idCat": p.categoria.idCat,
                    "nombreCat": p.categoria.nombreCat
                }
            }
            listJson.append(producto)

        mensaje = f"Total productos {len(productos)}"

        return {
            "mensaje": mensaje,
            "productos": listJson
        }
    except exc.SQLAlchemyError as err:
        mensaje = "Error al obtener los productos"

        return {
            "mensaje": mensaje
        }


@app.route("/consultarProductoJson", methods=["get"])
def consultarProductoJson():
    try:
        datos = request.get_json(force=True)
        idPro = int(datos["idPro"])
        producto = Producto.query.get(idPro)

        jsonPro = {
            "idPro": producto.idPro,
            "nombrePro": producto.nombrePro,
            "precioPro": producto.precioPro,
            "categoria": {
                "idCat": producto.categoria.idCat,
                "nombreCat": producto.categoria.nombreCat
            }
        }

        mensaje = "Producto Encontrado"

        return {
            "mensaje": mensaje,
            "producto": jsonPro
        }
    except exc.SQLAlchemyError as err:
        mensaje = "Error al obtener el producto"

        return {
            "mensaje": mensaje
        }


@app.route("/addProductoJson", methods=["post"])
def addProductoJson():
    try:
        datos = request.get_json(force=True)
        codigo = int(datos["codigo"])
        nombre = datos["nombre"]
        precio = int(datos["precio"])
        categoria = datos["categoria"]

        producto = Producto(codigoPro=codigo, nombrePro=nombre,
                            precioPro=precio, categoriaPro=categoria)

        db.session.add(producto)
        db.session.commit()

        mensaje = "Producto agregado"
    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje = str(ex)

    return {
        "mensaje": mensaje
    }


@app.route("/eliminarJson", methods=["post"])
def eliminarJson():
    try:
        datos = request.get_json(force=True)

        idPro = int(datos["idPro"])
        producto = Producto.query.get(idPro)

        db.session.delete(producto)
        db.session.commit()

        mensaje = "Producto Eliminado"

        nameFile = str(idPro) + ".jpg"
        os.remove(os.path.join(app.config["UPLOAD_FOLDER"]+"/" + nameFile))

    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje = str(ex)

    return {
        "mensaje": mensaje
    }


@app.route("/actualizarProductoJson", methods=["post"])
def actualizarProductoJson():
    try:

        datos = request.get_json(force=True)
        
        idPro = int(request.form["idPro"])
        producto = Producto.query.get(idPro)

        producto.codigoPro = request.form["codigo"]
        producto.nombrePro = request.form["nombre"]
        producto.precioPro = request.form["precio"]
        producto.categoriaPro = request.form["categoria"]

        db.session.commit()

        mensaje = "Producto Actualizado"

    except exc.SQLAlchemyError as ex:
        db.session.rollback()
        mensaje = str(ex)
        
    return {
        "mensaje": mensaje
    }