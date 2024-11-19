from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import Ingrediente, Producto, VentasTotales
from app import db

main = Blueprint('main', __name__)

ventas_dia=0
@main.route('/')
def index():
    
    productos = Producto.query.all()
    mas_rentable = max(productos, key=lambda producto: producto.calcular_rentabilidad()).nombre
    acumulado_ventas = VentasTotales.query.first().acumulado if VentasTotales.query.first() else 0.0
    return render_template('index.html', productos=productos, mas_rentable=mas_rentable, ventas_dia=acumulado_ventas)
    

@main.route('/ingredientes')
def ingredientes():
    
    ingredientes = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingredientes)

@main.route('/producto/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio_publico = request.form.get('precio')
        tipo = request.form.get('tipo')
        ingredientes_ids = request.form.getlist('ingredientes')  # Obtener IDs de los ingredientes seleccionados

        if not ingredientes_ids:
            flash('Seleccione Un Ingrediente', 'danger')
            return redirect(url_for('main.agregar_producto'))

        productos = Producto.query.all()
        if len(productos) == 4:
            flash('No Se Pueden Agregar Mas Productos (Max 4 Productos)', 'danger')
            return redirect(url_for('main.agregar_producto'))


        if len(ingredientes_ids) > 3:
            flash('Solo selecciona 3 ingredientes', 'danger')
            return redirect(url_for('main.agregar_producto'))

        # Crear el nuevo producto
        nuevo_producto = Producto(nombre=nombre, precio_publico=float(precio_publico), tipo=tipo)
        db.session.add(nuevo_producto)
        db.session.commit()

        # Relacionar ingredientes seleccionados con el producto
        for ingrediente_id in ingredientes_ids:
            ingrediente = Ingrediente.query.get(int(ingrediente_id))
            if ingrediente:
                nuevo_producto.ingredientes.append(ingrediente)
        
        db.session.commit()
        flash('Producto agregado con éxito', 'success')
        return redirect(url_for('main.index'))

    ingredientes = Ingrediente.query.all()  # Obtener todos los ingredientes
    return render_template('agregar_producto.html', ingredientes=ingredientes)


@main.route('/producto/vender', methods=['GET', 'POST'])
def vender_producto():
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        producto = Producto.query.get(producto_id)
        if producto:
            # Lógica para verificar si hay suficiente inventario
            for ingrediente in producto.ingredientes:
                cantidad_necesaria = 1 if ingrediente.es_vegetariano else 0.2
                if ingrediente.inventario < cantidad_necesaria:
                    flash(f'¡Oh no! Nos hemos quedado sin {ingrediente.nombre}', 'danger')
                    return redirect(url_for('main.vender_producto'))
                
                # Descontar la cantidad necesaria del inventario
                ingrediente.inventario -= cantidad_necesaria

            VentasTotales.incrementar_venta(producto.precio_publico)    
            db.session.commit()
            flash('¡Vendido!', 'success')
        else:
            flash('El producto no existe.', 'danger')
        return redirect(url_for('main.vender_producto'))

    productos = Producto.query.all()
    return render_template('vender_producto.html', productos=productos)

@main.route('/ingrediente/agregar', methods=['GET', 'POST'])
def agregar_ingrediente():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        precio = request.form.get('precio')
        calorias = request.form.get('calorias')
        inventario = request.form.get('inventario')
        es_vegetariano = request.form.get('es_vegetariano') == '1'
        tipo = request.form.get('tipo')
        
        nuevo_ingrediente = Ingrediente(nombre=nombre, precio=float(precio),calorias=int(calorias),inventario=int(inventario),es_vegetariano=es_vegetariano, tipo=tipo)
            
        # Guardar el nuevo ingrediente en la base de datos
        db.session.add(nuevo_ingrediente)
        db.session.commit()
        flash('Ingrediente agregado con éxito.', 'success')
        return redirect(url_for('main.agregar_ingrediente'))

    return render_template('agregar_ingrediente.html')

@main.route('/ingredientes/abastecer/<int:ingrediente_id>', methods=['GET','POST'])
def abastecer_ingrediente(ingrediente_id):
    if request.method == 'POST':
        #ingrediente_id = request.form.get('ingrediente_id')
        ingrediente = Ingrediente.query.get(ingrediente_id)

        if not ingrediente:
            flash('Seleccione Un Ingrediente', 'danger')
            return redirect(url_for('main.ingredientes'))
       
        ingrediente.abastecer()
        db.session.commit()
        flash(f'El inventario de {ingrediente.nombre} ha sido abastecido con éxito. {ingrediente.inventario}', 'success')
      

    ingre = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingre)


@main.route('/ingredientes/renovar/<int:ingrediente_id>', methods=['GET','POST'])
def renovar_ingrediente(ingrediente_id):
    if request.method == 'POST':
        #ingrediente_id = request.form.get('ingrediente_id')
        ingrediente = Ingrediente.query.get(ingrediente_id)
        
        # Verificar el tipo y abastecer según corresponda
        if ingrediente:
            ingrediente.renovar_inventario()
            db.session.commit()
            flash(f'El inventario de {ingrediente.nombre} ha sido renovado con éxito. {ingrediente.inventario}', 'success')
        else:
            flash('Error al renovar el ingrediente', 'danger')
            return redirect(url_for('main.ingredientes'))

    ingre = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingre)    


@main.route('/producto/editar/<int:producto_id>', methods=['POST'])
def editar_producto(producto_id):
    """Ruta para editar un producto existente."""
    producto = Producto.query.get(producto_id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('main.index'))

    # Obtener los nuevos datos del formulario
    nuevo_nombre = request.form.get('nombre')
    nuevo_precio = request.form.get('precio')

    # Actualizar el producto
    producto.nombre = nuevo_nombre
    producto.precio_publico = float(nuevo_precio)
    db.session.commit()
    flash('Producto actualizado con éxito', 'success')

    return redirect(url_for('main.index'))

@main.route('/producto/eliminar/<int:producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    """Ruta para eliminar un producto existente."""
    producto = Producto.query.get(producto_id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('main.index'))

    # Eliminar el producto
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado con éxito', 'success')

    return redirect(url_for('main.index'))