# 📝CRUD con Flask, MongoDB y Python  

## 🎯Objetivo

Este proyecto consiste en el desarrollo de una aplicación web básica que implementa las operaciones CRUD (*Create, Read, Update, Delete*) utilizando:  
- **Flask** como *microframework* web de Python.
- **MongoDB** como base de datos NoSQL para el almacenamiento de datos.
- **HTML** y **CSS** para la interfaz de usuario frontal.

El propósito es demostrar la integración de estas tecnologías en un entorno práctico, aplicando buenas prácticas de desarrollo. Además, se utiliza **Git y GitHub** para el control de versiones, siguiendo un flujo de trabajo organizado (commits descriptivos, estructura de repositorio clara, etc.)

## 🛠Requisitos previos

Asegúrate de tener instalado lo siguiente:

### 1. Python
- Versión 3.8 o superior.
  ```
      # Verificar instalación:
      python --version  # o python3 --version
  ```

### 2. PIP (Gestor de paquetes de Python)
- Debe estar incluido con Python. Actualízalo:
    ```
      pip install --upgrade pip
    ```
  
### 3. MongoDB
- Instala MongoDB Community Edition según tu SO:
[Windows/macOS/Linux: Guía oficial](https://www.mongodb.com/docs/manual/administration/install-community/ "Windows/macOS/Linux: Guía oficial")
- Inicia el servicio de MongoDB (normalmente se ejecuta en localhost:27017).

### 4. Dependencias de Python
- Ejecuta estos comandos uno por uno en la terminal (desde la raíz del proyecto):

```
    # Flask (framework web)
    pip install flask

    # PyMongo (conexión a MongoDB)
    pip install pymongo
```

## 🔧Configuración previa importante
### 1. Asegúrate que MongoDB esté corriendo:

```bash
# Windows (ejecutar como administrador):
net start MongoDB

# Linux/macOS:
sudo systemctl start mongod
```
### 2. Verifica las dependencias:

```bash
pip install flask
pip install pymongo
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
     - Conexión a MongoDB (`pymongo.MongoClient`).  
     - Configuración de colecciones (`db.usuarios`, `db.productos`).  

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

```python
app = Flask(__name__, template_folder='templates')  # Indicar carpeta de plantillas
app.config["MONGO_URI"] = "mongodb://localhost:27017/nombre_db"  # Conexión a MongoDB
```

### ⚙️ **Configuración de MongoDB** (en `database.py`):
   ```python
   # Para MongoDB LOCAL (default):
   MONGO_URI = 'mongodb://localhost:27017/'
   
   # Para MongoDB Atlas (en la nube):
    MONGO_URI = 'mongodb+srv://usuario:contraseña@clusterX.mongodb.net/?retryWrites=true&w=majority'
```
### 📌Notas adicionales
- Para Atlas, reemplaza:
	- usuario:contraseña por tus credenciales reales
	- clusterX por el nombre de tu cluster
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
- ✅ Integración MongoDB-Flask

### 📚Recursos útiles
- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Guía de MongoDB con Python](https://www.mongodb.com/docs/drivers/pymongo/)
- [Bootstrap para plantillas](https://getbootstrap.com/)

## ✨Créditos
*Desarrollado por Thomas Echeverry Rios*

*Con apoyo de Deepseek*



