import mysql.connector
from mysql.connector import Error

def dbConnection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Cambiar por tu usuario de MySQL
            password='',  # Cambiar por tu contraseña de MySQL
            database='db_crud'
        )
        return connection
    except Error as e:
        print(f'Error de conexión con la db: {e}')
        return None