# pedido.py
class Pedido:
    def __init__(self, numero_pedido, producto, cantidad, cliente):
        self.numero_pedido = numero_pedido
        self.producto = producto
        self.cantidad = cantidad
        self.cliente = cliente

    def toDBCollection(self):
        return {
            'numero_pedido': self.numero_pedido,
            'producto': self.producto,
            'cantidad': self.cantidad,
            'cliente': self.cliente,
        }