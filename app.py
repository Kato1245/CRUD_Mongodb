from flask import Flask, render_template, request, redirect, url_for, session, flash
import database as dbase
from product import Product
from usuario import Usuario
from pedido import Pedido
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

# Crear tablas si no existen
def create_tables():
    conn = dbase.dbConnection()
    if conn:
        cursor = conn.cursor()
        try:
            # Tabla usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    contraseña VARCHAR(255) NOT NULL
                )
            """)
            
            # Tabla productos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    precio DECIMAL(10, 2) NOT NULL,
                    cantidad INT NOT NULL
                )
            """)
            
            # Tabla pedidos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numero_pedido VARCHAR(255) NOT NULL,
                    producto VARCHAR(255) NOT NULL,
                    cantidad INT NOT NULL,
                    cliente VARCHAR(255) NOT NULL
                )
            """)
            
            # Insertar usuario vendedor si no existe
            cursor.execute("SELECT * FROM usuarios WHERE email = 'vendedor@gmail.com'")
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO usuarios (nombre, email, contraseña)
                    VALUES ('Vendedor', 'vendedor@gmail.com', 'vendedor123')
                """)
            
            conn.commit()
        except Error as e:
            print(f"Error al crear tablas: {e}")
        finally:
            cursor.close()
            conn.close()

# Crear tablas al iniciar
create_tables()

# Ruta principal
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
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                usuario = cursor.fetchone()
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
            except Error as e:
                print(f"Error al hacer login: {e}")
            finally:
                cursor.close()
                conn.close()
    return render_template('login.html')

# Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
                if cursor.fetchone():
                    flash('El usuario ya existe.', 'error')
                else:
                    cursor.execute("""
                        INSERT INTO usuarios (nombre, email, contraseña)
                        VALUES (%s, %s, %s)
                    """, (nombre, email, contraseña))
                    conn.commit()
                    flash('Registro exitoso. Inicia sesión.', 'success')
                    return redirect(url_for('login'))
            except Error as e:
                print(f"Error al registrar usuario: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
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
    
    conn = dbase.dbConnection()
    productos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener productos: {e}")
        finally:
            cursor.close()
            conn.close()
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
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO productos (nombre, precio, cantidad)
                    VALUES (%s, %s, %s)
                """, (nombre, precio, cantidad))
                conn.commit()
            except Error as e:
                print(f"Error al agregar producto: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
    return redirect(url_for('productos'))

# Eliminar producto (vendedor)
@app.route('/delete_product/<string:product_name>')
def deleteProduct(product_name):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    
    conn = dbase.dbConnection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM productos WHERE nombre = %s", (product_name,))
            conn.commit()
        except Error as e:
            print(f"Error al eliminar producto: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
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
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE productos 
                    SET nombre = %s, precio = %s, cantidad = %s
                    WHERE nombre = %s
                """, (nombre, precio, cantidad, product_name))
                conn.commit()
            except Error as e:
                print(f"Error al editar producto: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
    return redirect(url_for('productos'))

# Productos para usuarios normales
@app.route('/productos_usuario')
def productos_usuario():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] == 'vendedor@gmail.com':
        return redirect(url_for('productos'))
    
    conn = dbase.dbConnection()
    productos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener productos: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('productos_usuario.html', productos=productos)

# Realizar pedido (usuarios normales)
@app.route('/realizar_pedido', methods=['GET', 'POST'])
def realizar_pedido():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        producto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        cliente = session['email']

        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                # Verificar producto y cantidad
                cursor.execute("SELECT * FROM productos WHERE nombre = %s", (producto,))
                producto_db = cursor.fetchone()
                
                if producto_db and producto_db['cantidad'] >= cantidad:
                    # Crear número de pedido único
                    cursor.execute("SELECT COUNT(*) as total FROM pedidos")
                    total_pedidos = cursor.fetchone()['total']
                    numero_pedido = f"{total_pedidos}-{cliente}"

                    # Insertar pedido
                    cursor.execute("""
                        INSERT INTO pedidos (numero_pedido, producto, cantidad, cliente)
                        VALUES (%s, %s, %s, %s)
                    """, (numero_pedido, producto, cantidad, cliente))

                    # Actualizar cantidad de producto
                    nueva_cantidad = producto_db['cantidad'] - cantidad
                    cursor.execute("""
                        UPDATE productos 
                        SET cantidad = %s 
                        WHERE nombre = %s
                    """, (nueva_cantidad, producto))

                    conn.commit()
                    flash('Pedido realizado con éxito', 'success')
                else:
                    flash('No hay suficiente cantidad disponible o el producto no existe', 'error')
            except Error as e:
                print(f"Error al realizar pedido: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('productos_usuario'))

    # GET: Mostrar productos disponibles
    conn = dbase.dbConnection()
    productos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener productos: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('realizar_pedido.html', productos=productos)

# Pedidos para usuarios normales
@app.route('/pedidos_usuario')
def pedidos_usuario():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] == 'vendedor@gmail.com':
        return redirect(url_for('pedidos'))
    
    conn = dbase.dbConnection()
    pedidos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pedidos WHERE cliente = %s", (session['email'],))
            pedidos = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener pedidos: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('pedidos_usuario.html', pedidos=pedidos)

# Pedidos (vista del vendedor)
@app.route('/pedidos')
def pedidos():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('pedidos_usuario'))
    
    conn = dbase.dbConnection()
    pedidos = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM pedidos")
            pedidos = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener pedidos: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

# Agregar pedido (vendedor)
@app.route('/pedidos', methods=['POST'])
def addPedido():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('pedidos_usuario'))
    
    numero_pedido = request.form['numero_pedido']
    producto = request.form['producto']
    cantidad = request.form['cantidad']
    cliente = request.form['cliente']
    
    if numero_pedido and producto and cantidad and cliente:
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO pedidos (numero_pedido, producto, cantidad, cliente)
                    VALUES (%s, %s, %s, %s)
                """, (numero_pedido, producto, cantidad, cliente))
                conn.commit()
            except Error as e:
                print(f"Error al agregar pedido: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
    return redirect(url_for('pedidos'))

# Eliminar pedido (vendedor)
@app.route('/delete_pedido/<string:numero_pedido>')
def deletePedido(numero_pedido):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('pedidos_usuario'))
    
    conn = dbase.dbConnection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM pedidos WHERE numero_pedido = %s", (numero_pedido,))
            conn.commit()
        except Error as e:
            print(f"Error al eliminar pedido: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
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
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE pedidos 
                    SET producto = %s, cantidad = %s, cliente = %s
                    WHERE numero_pedido = %s
                """, (producto, cantidad, cliente, numero_pedido))
                conn.commit()
            except Error as e:
                print(f"Error al editar pedido: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
    return redirect(url_for('pedidos'))

# Usuarios (vista del vendedor)
@app.route('/usuarios')
def usuarios():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    
    conn = dbase.dbConnection()
    usuarios = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
        except Error as e:
            print(f"Error al obtener usuarios: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

# Eliminar usuario (vendedor)
@app.route('/delete_usuario/<string:usuario_nombre>')
def deleteUsuario(usuario_nombre):
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['email'] != 'vendedor@gmail.com':
        return redirect(url_for('productos_usuario'))
    
    conn = dbase.dbConnection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE nombre = %s", (usuario_nombre,))
            conn.commit()
            flash('Usuario eliminado correctamente', 'success')
        except Error as e:
            print(f"Error al eliminar usuario: {e}")
            flash('Error al eliminar usuario', 'error')
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('usuarios'))

# Perfil
@app.route('/perfil')
def perfil():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = dbase.dbConnection()
    usuario = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (session['email'],))
            usuario = cursor.fetchone()
        except Error as e:
            print(f"Error al obtener perfil: {e}")
        finally:
            cursor.close()
            conn.close()
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
        conn = dbase.dbConnection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE usuarios 
                    SET nombre = %s, email = %s, contraseña = %s
                    WHERE email = %s
                """, (nombre, email, contraseña, session['email']))
                conn.commit()
                session['username'] = nombre
                session['email'] = email
                flash('Perfil actualizado correctamente', 'success')
            except Error as e:
                print(f"Error al actualizar perfil: {e}")
                flash('Error al actualizar perfil', 'error')
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
    return redirect(url_for('perfil'))

# Eliminar perfil
@app.route('/delete_perfil')
def deletePerfil():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = dbase.dbConnection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE email = %s", (session['email'],))
            conn.commit()
            session.pop('username', None)
            session.pop('email', None)
            flash('Tu cuenta ha sido eliminada', 'success')
        except Error as e:
            print(f"Error al eliminar perfil: {e}")
            flash('Error al eliminar cuenta', 'error')
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)