from . import db

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=False)

    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    ingredientes = db.relationship('Ingrediente', secondary='producto_ingrediente', backref='productos')

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.ingredientes)

    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self.ingredientes) * 0.95

    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()

producto_ingrediente = db.Table('producto_ingrediente',
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
)
