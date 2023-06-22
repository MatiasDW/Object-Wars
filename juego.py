import os
from jugador import Jugador
from unidad import Soldado, Arquero, Caballero
import sys

N_VIDAS = 20
MONEDAS_TURNO = 10
BONUS_DANO = 1.5


class Juego():

    def __init__(self, nombre_jugador1,  nombre_jugador2):
        """Creadora"""
        self.jugador1 = Jugador(nombre=nombre_jugador1,
                                puntos_vida=20)
        self.jugador2 = Jugador(nombre=nombre_jugador2,
                                puntos_vida=20)

    @staticmethod
    def _elegir_opcion(options):
        """Muestra por pantalla la lista de opciones enumeradas y retorna el número de opción elegida.
         options es una lista de strings"""
        print("Elige una opción:")
        for idx, element in enumerate(options):
            print("{}) {}".format(idx+1, element))
        i = input("Introduce un número: ")
        try:
            if 0 < int(i) <= len(options):
                return int(i)
        except:
            pass
        return None

    def _turno(self, jugador):
        f"""Se le añaden {MONEDAS_TURNO} al jugador, se le muestran las opciones de compra hasta que decida finalizar el turno"""
        pass

    def _finalizar(self, jugador_ganador):
        """Finaliza la partida mostrando como ganador al jugador_ganador"""
        self._clear_screen()

        print(f"""FIN DEL JUEGO
El jugador ganador es {jugador_ganador.nombre}""")
        quit()

    @staticmethod
    def _clear_screen():
        if(os.name == 'posix'):
            os.system('clear')
        # else screen will be cleared for windows
        else:
            os.system('cls')
            pass

    def loop(self):
        "Loop del juego, se ejecuta hasta finalizar la partida"
        ronda = 0
        while(True):
            ronda += 1
            self._turno(self.jugador1)
            self._clear_screen()
            self._turno(self.jugador2)
            self._batalla()

            # limitación para permitir tests de funcionalidad sin implementación
            if ronda == 100:
                break

    def _daño_al_jugador(self, defensor, atacante):
        """
        El defensor recibe un ataque de cada unidad del atacante, si el defensor se queda sin
        puntos de vida, llama a la función _finalizar.
        """
        pass

    @staticmethod
    def _calcular_bonus(atacante, defensor):
        """Devuelve el bonus de ataque que tiene el atacante contra el defensor, se debe usar
         la función isinstace(instancia, clase) para implementarla"""

    def _batalla(self):
        """Realiza una batalla entre las unidades del jugador1 y el jugador2. 
        La batalla se desarrolla en combates 1 vs 1, siempre entre las unidades más antiguas de cada jugador.
        Durante un combate, las dos unidades pierdan tantos puntos de vida como puntos de ataque tenga la unidad adversaria.
        Si una unidad sobrevive a un combate, ésta participará en el siguiente combate, la batalla continua mientras ambos jugadores
         tengan unidades disponibles. 
        Cuando a un jugador no le queden más unidades, recibe un ataque de cada unidad enemiga remaniente.
        Al acabar, los jugadores hacen descansar a sus unidades.
        """
        pass

    @classmethod
    def mensaje_bienvenida(self):
        print(f"""
Bienvenido a ObjectWars
Este juego es un juego para dos jugadores. Lo que un jugador realiza durante su turno es secreto, por lo que el otro jugador no debe mirar las acciones que realize el otro \
jugador durante su turno.

El objectivo del juego es dejar el enemigo sin puntos de vida, al empezar cada jugador dispone de {N_VIDAS}.

Durante un turno el jugador puede comprar unidades.

Al empejar un turno cada jugador recibe {MONEDAS_TURNO} mondedas.

Despues de que ambos jugadores acaben sus turnos sus unidades entraran en combate. Si un jugador no tiene unidades, o son derrotadas, recibirá el daño en sus puntos de vida.

Existen tres tipologias de unidades: soldados, arqueros y caballeros. Las unidades tienen un bonus de {BONUS_DANO} de daño siguiendo la siguiente jerarquía:
soldado -> arquero -> caballero -> soldado


    
    """)


if __name__ == "__main__":
    Juego.mensaje_bienvenida()
    nombre1 = input("Introduce el nombre del jugador1: ")
    nombre2 = input("Introduce el nombre del jugador2: ")
    juego = Juego(nombre1, nombre2)
    juego.loop()
