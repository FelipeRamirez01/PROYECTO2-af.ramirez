
from models.ingrediente import Ingrediente
from models.producto import Producto
import unittest


class TestHeladeria(unittest.TestCase):

    def setUp(self):

        """Configurar un entorno inicial para cada prueba."""
        self.ingrediente1 = Ingrediente(id=1, nombre='Helado de Fresa', precio=1200, calorias=80, inventario=10, es_vegetariano=True, tipo="base")
        self.ingrediente2 = Ingrediente(id=2, nombre='Chispas de Chocolate', precio=500, calorias=150, inventario=5, es_vegetariano=False, tipo="complemento")
        self.ingrediente3 = Ingrediente(id=3,nombre='Maní Japonés', precio=900, calorias=300, inventario=2, es_vegetariano=False, tipo="complemento")
        self.producto = Producto(id=1, nombre='Copa de Fresa', precio_publico=7500, ingredientes=[self.ingrediente1, self.ingrediente2, self.ingrediente3])
        self.producto2 = Producto(id=2,nombre='Malteada Chocoespacial', precio_publico=9500,ingredientes=[self.ingrediente1, self.ingrediente2])
      
    def test_es_sano(self):
        """Probar si un ingrediente es sano."""
        self.assertTrue(self.ingrediente1.es_sano())
        self.assertFalse(self.ingrediente2.es_sano())

    def test_abastecer_ingrediente(self):
        """Probar abastecimiento de ingredientes."""
        cantidad_inicial = self.ingrediente1.inventario
        abastecer= self.ingrediente1.abastecer(self.ingrediente1.tipo)
        self.assertEqual(abastecer, cantidad_inicial + 5)

    def test_renovar_inventario_complemento(self):
        """Probar la renovación de inventario para los complementos."""
        self.ingrediente3.renovar_inventario()
        self.ingrediente3.abastecer(self.ingrediente3.tipo) 
        self.assertEqual(self.ingrediente3.inventario, 10)

    def test_calcular_calorias(self):
        """Probar el cálculo de calorías de un producto."""
        calorias = self.producto.calcular_calorias()
        expected_calorias = sum([ingrediente.calorias for ingrediente in self.producto.ingredientes]) + 200
        self.assertAlmostEqual(calorias, expected_calorias)

    def test_calcular_costo_produccion(self):
        """Probar el cálculo del costo de producción de un producto."""
        costo = self.producto.calcular_costo()
        expected_costo = sum([ingrediente.precio for ingrediente in self.producto.ingredientes])+500
        self.assertEqual(costo, expected_costo)

    def test_calcular_rentabilidad(self):
        """Probar el cálculo de la rentabilidad de un producto."""
        rentabilidad = self.producto.calcular_rentabilidad()
        expected_rentabilidad = self.producto.precio_publico - self.producto.calcular_costo()
        self.assertEqual(rentabilidad, expected_rentabilidad)

    def test_encontrar_producto_mas_rentable(self):
        """Probar encontrar el producto más rentable."""       
        productos = [self.producto, self.producto2]
        mas_rentable = max(productos, key=lambda p: p.calcular_rentabilidad())
        self.assertEqual(mas_rentable.nombre, self.producto2.nombre)

    def test_vender_producto(self):
        """Probar la venta de un producto."""
        cantidad_inicial = [ingrediente.inventario for ingrediente in self.producto.ingredientes]
        venta_exitosa = True
        for ingrediente in self.producto.ingredientes:
            cantidad_necesaria = 2
            if ingrediente.inventario < cantidad_necesaria:
                venta_exitosa = False
                break
            ingrediente.inventario -= cantidad_necesaria
        self.assertTrue(venta_exitosa)
        for i, ingrediente in enumerate(self.producto.ingredientes):
            self.assertAlmostEqual(ingrediente.inventario, cantidad_inicial[i]-2)

if __name__ == '__main__':
    unittest.main()
