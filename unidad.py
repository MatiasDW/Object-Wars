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
     def __init__(self):
        super().__init__()
        self.coste = 5
        self.puntos_vida = MAX_VIDA
        self.puntos_ataque = 3

    def descansar(self):
        self.puntos_vida += 5


class Arquero():
    """ Unidad Arquero, tiene un coste de 6 monedas, tiene 8 puntos de ataque y restaura 2 puntos de vida al decansar
    Los arqueros atacan 1 de cada 2 veces ya que deben recargar, empiezan la partida sin estar preparados para atacar"""
    def __init__(self):
            super().__init__()
            self.coste = 6
            self.puntos_vida = MAX_VIDA
            self.puntos_ataque = 8
            self.preparado = False

        def descansar(self):
            self.puntos_vida += 2
            self.preparado = True

        def atacar(self):
            if self.preparado:
                self.preparado = False
                return self.puntos_ataque
            else:
                return 0

class Caballero():
    """ Unidad Caballero, tiene un coste de 9 monedas, tiene 5 puntos de ataque, y al descansar no restaura puntos de vida"""
     def __init__(self):
        super().__init__()
        self.coste = 9
        self.puntos_vida = MAX_VIDA
        self.puntos_ataque = 5

    def descansar(self):
        # Los caballeros no restauran puntos de vida al descansar
        pass

    def atacar(self):
        return self.puntos_ataque