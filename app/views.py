from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Ingrediente, Producto

main = Blueprint('main', __name__)

@main.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)
    

@main.route('/ingredientes')
def ingredientes():
    ingredientes = Ingrediente.query.all()
    return render_template('ingredientes.html', ingredientes=ingredientes)

@main.route('/producto/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio_publico = request.form.get('precio')
        ingredientes_ids = request.form.getlist('ingredientes')  # Obtener IDs de los ingredientes seleccionados

        # Crear el nuevo producto
        nuevo_producto = Producto(nombre=nombre, precio_publico=float(precio_publico))
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
            db.session.commit()
            flash('¡Producto vendido con éxito!', 'success')
        else:
            flash('El producto no existe.', 'danger')
        return redirect(url_for('main.vender_producto'))

    productos = Producto.query.all()
    return render_template('vender_producto.html', productos=productos)

