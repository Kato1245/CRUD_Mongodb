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