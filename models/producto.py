from app import db

class Producto():
    def __init__(self, id, nombre, precio_publico, ingredientes:list):
        self.id = id
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.ingredientes = ingredientes
    
    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.ingredientes) + 500

    def calcular_calorias(self):
        return sum(ingrediente.calorias for ingrediente in self.ingredientes) + 200

    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()
