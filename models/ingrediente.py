from app import db

class Ingrediente():
    def __init__(self, id, nombre, precio, calorias, inventario, es_vegetariano, tipo):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.calorias = calorias
        self.inventario = inventario
        self.es_vegetariano = es_vegetariano
        self.tipo = tipo


    def es_sano(self):
        return self.calorias < 100 or self.es_vegetariano
    
    def renovar_inventario(self):
        self.inventario = 0

          
    def abastecer(self, tipo):
        if tipo == "base":
            self.inventario += 5
            return self.inventario
        else:
            self.inventario += 10
            return self.inventario

