# declara la clase accion para guardar los valores obtenidos de la web
#  en un objeto que pueda ser manipulado, guaradado, etc

class Accion:
    def __init__(self, nombre, precio, volumen):
        self.nombre = nombre
        self.precio = precio
        self.volumen = volumen


    def __str__(self):
        return f"Acción: {self.nombre} | Precio: {self.precio} CLP | Volumen: {self.volumen[1]} | Monto: {self.volumen[2]}"