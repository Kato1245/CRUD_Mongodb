# 📝CRUD con Flask, MySQL y Python  

## 🎯Objetivo

Este proyecto consiste en el desarrollo de una aplicación web básica que implementa las operaciones CRUD (*Create, Read, Update, Delete*) utilizando:  
- **Flask** como *microframework* web de Python.
- **MySQL** como base de datos relacional para el almacenamiento de datos.
- **HTML** y **BOOTSTRAP** para la interfaz de usuario.

## 🛠Requisitos previos

Asegúrate de tener instalado lo siguiente:

### 1. Python
- Versión 3.8 o superior.
```shell
# Verificar instalación:
python --version  # o python3 --version
```

### 2. PIP (Gestor de paquetes de Python)
- Debe estar incluido con Python. Actualízalo:
```sh
pip install --upgrade pip
```

### 3. MySQL
- Instala MySQL Server según tu SO:
	- [Windows/macOS/Linux: Guía oficial](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/ "Windows/macOS/Linux: Guía oficial")
- Inicia el servicio MySQL (normalmente en localhost:3306)

### 4. Dependencias de Python
```shell
# Flask (framework web)
pip install flask

# MySQL Connector
pip install mysql-connector-python
```

## 🔧Configuración previa importante

### 1. Configuración de MySQL
1. Crear la base de datos:
```sql
CREATE DATABASE db_crud;
```

2. Configurar credenciales en database.py:
```python
connection = mysql.connector.connect(
    host='localhost',
    user='root',      # Cambiar por tu usuario
    password='',      # Cambiar por tu contraseña
    database='db_crud'
)
```

### 2. Iniciar MySQL
```bash
# Linux/macOS:
sudo systemctl start mysql

# Windows (ejecutar como administrador):
net start MySQL80
```

## 📂Estructura del Proyecto
```plaintext
.
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── perfil.html
│   ├── productos.html
│   ├── productos_usuario.html
│   ├── pedidos.html
│   ├── pedidos_usuario.html
│   └── realizar_pedido.html
├── app.py
├── database.py
├── usuario.py
├── product.py
└── pedido.py
```

### 🔍Explicación detallada:
1. **Carpeta `templates/`**  
   Contiene todas las vistas HTML renderizadas por Flask.
   - `login.html` y `register.html`: Autenticación de usuarios.
   - `productos.html` (admin) vs `productos_usuario.html`: Diferenciación de permisos.
   - `realizar_pedido.html`: Formulario interactivo para nuevos pedidos.

2. **Archivos principales en raíz**
   - `app.py`:
     - Configuración inicial de Flask (`app = Flask(__name__)`).
     - Definición de rutas (`@app.route`).
     - Lógica de controladores (ej: `@app.route('/productos')`).
   - `database.py`:
     -Conexión a MySQL (`mysql.connector`).
     -  Configuración de credenciales.

3. **Modelos en raíz**
	- `usuario.py`:  
     ```python
	    class Usuario:
		    def __init__(self, nombre, email, contraseña):
			  self.nombre = nombre
			  self.email = email
			  self.contraseña = contraseña

		    def toDBCollection(self):
			  return{
				  'nombre': self.nombre,
				  'email': self.email,
				  'contraseña': self.contraseña,
			  }
     ```

   - `product.py` y `pedido.py`: Siguen patrón similar con sus respectivos campos.

### ⚙️Configuración clave en `app.py`:
```sql
# Creación de tablas al iniciar
def create_tables():
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            contraseña VARCHAR(255) NOT NULL
        )
    """)
    # ... (resto de tablas)
```

### 📌Notas adicionales
- **Usuario administrador por defecto**: 
   - Email: `vendedor@gmail.com`
   - Contraseña: `vendedor123`
   - **¡Debe estar registrado en la base de datos!**
   - Este usuario tiene acceso privilegiado a:
     - Gestión completa de productos
     - Visualización de todos los pedidos
     - Administración de usuarios

## 🚀Ejecutar el Proyecto

### Método recomendado (con depurador de VS Code)
1. **Abre el archivo `app.py`** en Visual Studio Code
2. **Haz clic en el botón "Run"** (triángulo verde) o presiona `F5`
3. **Selecciona "Python File"** como configuración de depuración
4. **Espera a que aparezca** este mensaje en la terminal:
	- Running on http://127.0.0.1:4000/ (Presione CTRL+C para salir)
5. **Abre tu navegador** en: 🌐 [http://localhost:4000](http://localhost:4000)

### Método alternativo (terminal manual)
```bash
# Desde la raíz del proyecto ejecuta:
python app.py
```

## 🏁Conclusión
Este proyecto implementa un CRUD completo con:
- ✅ Autenticación de usuarios
- ✅ Gestión de productos y pedidos
- ✅ Integración Flask-MySQL

### 📚Recursos útiles
- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/ "MySQL Connector/Python")
- [Bootstrap para plantillas](https://getbootstrap.com/)

## ✨Créditos
*Desarrollado por Thomas Echeverry Rios*

*Con apoyo de Deepseek*
