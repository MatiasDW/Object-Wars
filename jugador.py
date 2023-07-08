from operator import concat
from unidad import *


class Jugador():
    "Un Jugador tiene un nombre, puntos_vida, monedas y unidades. Un jugador no puede tener deudas, es decir, no puede tener un número de monedas negativo"

    def __init__(self, nombre, puntos_vida=20):
        """
        Creadora de la clase Jugador.
        
        Parámetros:
        - nombre: Nombre del jugador.
        - puntos_vida: Puntos de vida del jugador (por defecto: 20).
        """
        self.nombre = nombre
        self.puntos_vida = puntos_vida
        self.monedas = 0
        self.unidades = []

    def descansar(self):
        """
        Hace que la primera unidad del jugador descanse si existe.
        """
        if self.unidades:
            self.unidades[0].descansar()

    def get_monedas(self):
        """
        Devuelve el número de monedas actual del jugador.
        
        Retorna:
        - Número de monedas del jugador.
        """
        return self.monedas

    def set_monedas(self, value):
        """
        Modifica el número de monedas del jugador por el valor dado.
        
        Parámetros:
        - value: Nuevo valor de monedas a establecer.
        """
        if value >= 0:
            self.monedas = value
        else:
            print("No se permiten monedas negativas.")
