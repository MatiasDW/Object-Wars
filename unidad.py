from abc import ABC, abstractmethod

MAX_VIDA = 10


class Unidad():
    """Clase abstracta que modela una unidad"""

    def __init__(self):
        """Creadora del objecto Unidad"""
        pass

    def descansar(self):
        """ Metodo abastracto, restaura puntos de vida a la unidad"""
        pass

    def atacar(self):
        """Este metodo debe ser usado para consultar los puntos de ataque, en caso de que la unidad este atacando"""
        pass


class Soldado():
    """Unidad soldado, tiene un coste de 5 monedas, tiene 3 puntos de ataque y restaura 5 puntos de vida al descansar"""


class Arquero():
    """ Unidad Arquero, tiene un coste de 6 monedas, tiene 8 puntos de ataque y restaura 2 puntos de vida al decansar
    Los arqueros atacan 1 de cada 2 veces ya que deben recargar, empiezan la partida sin estar preparados para atacar"""


class Caballero():
    """ Unidad Caballero, tiene un coste de 9 monedas, tiene 5 puntos de ataque, y al descansar no restaura puntos de vida"""
