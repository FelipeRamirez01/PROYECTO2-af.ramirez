from app import db

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.String(20), nullable=False)


    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano
    
    def renovar_inventario(self):
        self.inventario = 0

          
    def abastecer(self):
        if self.tipo=="base":
            self.inventario += 5
        else:
            self.inventario += 10


class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    ingredientes = db.relationship('Ingrediente', secondary='producto_ingrediente', backref='productos')

    def calcular_costo(self):
        if self.tipo == "copa":
            return sum(ingrediente.precio for ingrediente in self.ingredientes)
        else:
            return sum([ingrediente.precio for ingrediente in self.ingredientes]) + 500 

    def calcular_calorias(self):
        if self.tipo == "copa":
            return round(sum(ingrediente.calorias for ingrediente in self.ingredientes) * 0.95,2)
        else:
            return sum([ingrediente.calorias for ingrediente in self.ingredientes]) + 200    

    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
    
   



producto_ingrediente = db.Table('producto_ingrediente',
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
)


class VentasTotales(db.Model):
    __tablename__ = 'ventas_totales'
    id = db.Column(db.Integer, primary_key=True)
    acumulado = db.Column(db.Float, default=0.0)  # Acumulado de ventas

    @staticmethod
    def incrementar_venta(cantidad):
        venta = VentasTotales.query.first()
        if not venta:
            venta = VentasTotales(acumulado=cantidad)
            db.session.add(venta)
        else:
            venta.acumulado += cantidad
        db.session.commit()