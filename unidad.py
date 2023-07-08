from abc import ABC, abstractmethod

MAX_VIDA = 10


class Unidad():
    """Clase abstracta que modela una unidad"""

    def __init__(self):
        """Creadora del objeto Unidad"""
        pass

    def descansar(self):
        """Restaura puntos de vida a la unidad"""
        pass

    def atacar(self, unidad_enemiga):
        """Consulta los puntos de ataque de la unidad y aplica bonificaciones"""
        pass


class Soldado(Unidad):
    """Unidad soldado, tiene un coste de 5 monedas, tiene 3 puntos de ataque y restaura 5 puntos de vida al descansar"""

     def __init__(self):
        super().__init__()
        self.coste = 5
        self.puntos_vida = MAX_VIDA
        self.puntos_ataque = 3

    def descansar(self):
        self.puntos_vida += 5

    def atacar(self, unidad_enemiga):
        bonus = self._calcular_bonus(unidad_enemiga)
        return int(self.puntos_ataque * bonus)

    def _calcular_bonus(self, unidad_enemiga):
        if isinstance(unidad_enemiga, Arquero):
            return 1.5
        elif isinstance(unidad_enemiga, Caballero):
            return 0.5
        else:
            return 1.0


class Arquero(Unidad):
    """Unidad Arquero, tiene un coste de 6 monedas, tiene 8 puntos de ataque y restaura 2 puntos de vida al descansar.
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

    def atacar(self, unidad_enemiga):
        if self.preparado:
            self.preparado = False
            bonus = self._calcular_bonus(unidad_enemiga)
            return int(self.puntos_ataque * bonus)
        else:
            return 0

    def _calcular_bonus(self, unidad_enemiga):
        if isinstance(unidad_enemiga, Caballero):
            return 1.5
        elif isinstance(unidad_enemiga, Soldado) or isinstance(unidad_enemiga, Arquero):
            return 1.0


class Caballero(Unidad):
    """Unidad Caballero, tiene un coste de 9 monedas, tiene 5 puntos de ataque y no restaura puntos de vida al descansar"""

    def __init__(self):
        super().__init__()
        self.coste = 9
        self.puntos_vida = MAX_VIDA
        self.puntos_ataque = 5

    def descansar(self):
        # Los caballeros no restauran puntos de vida al descansar
        pass

    def atacar(self, unidad_enemiga):
        bonus = self._calcular_bonus(unidad_enemiga)
        return int(self.puntos_ataque * bonus)

    def _calcular_bonus(self, unidad_enemiga):
        if isinstance(unidad_enemiga, Soldado):
            return 1.5
        elif isinstance(unidad_enemiga, Arquero):
            return 1.5
        elif isinstance(unidad_enemiga, Caballero):
            return 1.0
