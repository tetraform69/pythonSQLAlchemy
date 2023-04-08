from app import db


class Producto(db.Model):
    __tablename__ = "productos"
    idPro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigoPro = db.Column(db.Integer, unique=True, nullable=False)
    nombrePro = db.Column(db.String(50), nullable=False)
    precioPro = db.Column(db.Integer, nullable=False)
    #* se crea el campo foreign
    categoriaPro = db.Column(db.Integer, db.ForeignKey(
        "categorias.idCat"), nullable=False)
    #! se crea la relacion
    categoria = db.relationship(
        "Categoria", backref=db.backref("categorias", lazy=True))

    def __repr__(self) -> str:
        return f"({self.codigoPro}, {self.nombrePro}, {self.precioPro}, {self.categoria.nombreCat})"
