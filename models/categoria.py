from app import db


class Categoria(db.Model):
    __tablename__ = "categorias"
    idCat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreCat = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return self.nombreCategoria
