from flask import Flask, render_template, request, redirect, url_for, session, flash
import database as dbase
from product import Product
from usuario import Usuario
from pedido import Pedido

db = dbase.dbConnection()

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Clave secreta para manejar sesiones

# Ruta principal (redirige al login)
@app.route('/')
def index():
    if 'username' in session:
        if session['email'] == 'vendedor@gmail.com':
            return redirect(url_for('productos'))
        else:
            return redirect(url_for('productos_usuario'))
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = db['usuarios'].find_one({'email': email})
        if usuario:
            if usuario['contraseña'] == contraseña:
                session['username'] = usuario['nombre']
                session['email'] = usuario['email']
                if email == 'vendedor@gmail.com':
                    return redirect(url_for('productos'))
                else:
                    return redirect(url_for('productos_usuario'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Esta cuenta no existe. Por favor, regístrate.', 'error')
    return render_template('login.html')

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        if db['usuarios'].find_one({'email': email}):
            flash('El usuario ya existe.', 'error')
        else:
            usuario = Usuario(nombre, email, contraseña)
            db['usuarios'].insert_one(usuario.toDBCollection())
            flash('Registro exitoso. Inicia sesión.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Productos (vista del vendedor)
@app.route('/productos')
def productos():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    productos = db['productos'].find()
    return render_template('productos.html', productos=productos)

# Agregar producto (vendedor)
@app.route('/products', methods=['POST'])
def addProduct():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    if nombre and precio and cantidad:
        product = Product(nombre, precio, cantidad)
        db['productos'].insert_one(product.toDBCollection())
    return redirect(url_for('productos'))

# Eliminar producto (vendedor)
@app.route('/delete_product/<string:product_name>')
def deleteProduct(product_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    db['productos'].delete_one({'nombre': product_name})
    return redirect(url_for('productos'))

# Editar producto (vendedor)
@app.route('/edit_product/<string:product_name>', methods=['POST'])
def editProduct(product_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    if nombre and precio and cantidad:
        db['productos'].update_one(
            {'nombre': product_name},
            {'$set': {'nombre': nombre, 'precio': precio, 'cantidad': cantidad}}
        )
    return redirect(url_for('productos'))

# Productos para usuarios normales
@app.route('/productos_usuario')
def productos_usuario():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] == 'vendedor@gmail.com':
        return redirect(url_for('productos'))
    productos = db['productos'].find()
    return render_template('productos_usuario.html', productos=productos)

# Pedidos para usuarios normales
@app.route('/pedidos_usuario')
def pedidos_usuario():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] == 'vendedor@gmail.com':
        return redirect(url_for('pedidos'))
    pedidos = db['pedidos'].find({'cliente': session['email']})
    return render_template('pedidos_usuario.html', pedidos=pedidos)

# Pedidos (vista del vendedor)
@app.route('/pedidos')
def pedidos():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('pedidos_usuario'))
    pedidos = db['pedidos'].find()
    return render_template('pedidos.html', pedidos=pedidos)

# Agregar pedido
@app.route('/pedidos', methods=['POST'])
def addPedido():
    if 'username' not in session:
        return redirect(url_for('login'))
    numero_pedido = request.form['numero_pedido']
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    cliente = request.form['cliente']
    if numero_pedido and producto and cantidad and cliente:
        pedido = Pedido(numero_pedido, producto, cantidad, cliente)
        db['pedidos'].insert_one(pedido.toDBCollection())
    return redirect(url_for('pedidos'))

# Eliminar pedido (vendedor)
@app.route('/delete_pedido/<string:numero_pedido>')
def deletePedido(numero_pedido):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('pedidos_usuario'))
    db['pedidos'].delete_one({'numero_pedido': numero_pedido})
    return redirect(url_for('pedidos'))

# Editar pedido (vendedor)
@app.route('/edit_pedido/<string:numero_pedido>', methods=['POST'])
def editPedido(numero_pedido):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('pedidos_usuario'))
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    cliente = request.form['cliente']
    if producto and cantidad and cliente:
        db['pedidos'].update_one(
            {'numero_pedido': numero_pedido},
            {'$set': {'producto': producto, 'cantidad': cantidad, 'cliente': cliente}}
        )
    return redirect(url_for('pedidos'))

# Usuarios (vista del vendedor)
@app.route('/usuarios')
def usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    usuarios = db['usuarios'].find()
    return render_template('usuarios.html', usuarios=usuarios)

# Eliminar usuario (vendedor)
@app.route('/delete_usuario/<string:usuario_nombre>')
def deleteUsuario(usuario_nombre):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    db['usuarios'].delete_one({'nombre': usuario_nombre})
    return redirect(url_for('usuarios'))

# Editar usuario (vendedor)
@app.route('/edit_usuario/<string:usuario_nombre>', methods=['POST'])
def editUsuario(usuario_nombre):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    nombre = request.form['nombre']
    email = request.form['email']
    contraseña = request.form['contraseña']
    if nombre and email and contraseña:
        db['usuarios'].update_one(
            {'nombre': usuario_nombre},
            {'$set': {'nombre': nombre, 'email': email, 'contraseña': contraseña}}
        )
    return redirect(url_for('usuarios'))

# Perfil
@app.route('/perfil')
def perfil():
    if 'username' not in session:
        return redirect(url_for('login'))
    usuario = db['usuarios'].find_one({'email': session['email']})
    return render_template('perfil.html', usuario=usuario)

# Actualizar perfil
@app.route('/update_perfil', methods=['POST'])
def updatePerfil():
    if 'username' not in session:
        return redirect(url_for('login'))
    nombre = request.form['nombre']
    email = request.form['email']
    contraseña = request.form['contraseña']
    if nombre and email and contraseña:
        db['usuarios'].update_one(
            {'email': session['email']},
            {'$set': {'nombre': nombre, 'email': email, 'contraseña': contraseña}}
        )
        session['username'] = nombre
        session['email'] = email
        flash('Perfil actualizado correctamente', 'success')
    return redirect(url_for('perfil'))

# Eliminar perfil
@app.route('/delete_perfil')
def deletePerfil():
    if 'username' not in session:
        return redirect(url_for('login'))
    db['usuarios'].delete_one({'email': session['email']})
    session.pop('username', None)
    session.pop('email', None)
    flash('Tu cuenta ha sido eliminada', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)