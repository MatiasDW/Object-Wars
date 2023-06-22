
from operator import concat
from unidad import *


class Jugador():
    "Un Jugador tiene un nombre, puntos_vida, monedas y unidades. Un jugador no puede deudas, es decir, no puede tener un numero de monedas negativo"

    def __init__(self, nombre, puntos_vida=20):
        pass

    def descansar(self):
        """Hace que la primera unidad, si la hay, descanse"""
        pass

    def get_monedas(self):
        """Devuelve el numero de monedas actual del jugador"""
        pass

    def set_monedas(self, value):
        """Modifica el numero de monedas por el valor value"""
        pass
