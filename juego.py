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
    #Realiza el turno del jugador. Permite al jugador comprar unidades y finalizar su turno.

        print(f"Turno de {jugador.nombre}")
        print(f"Tienes {jugador.get_monedas()} monedas disponibles.")
    
    while True:
        print("Elige una opción:")
        print("1) Comprar unidad")
        print("2) Finalizar turno")
        opcion = input("Introduce el número de opción: ")
        
        if opcion == "1":
            self._comprar_unidad(jugador)
        elif opcion == "2":
            break
        else:
            print("Opción inválida. Por favor, elige una opción válida.")
    
        print(f"{jugador.nombre} ha finalizado su turno.")


    def _comprar_unidad(self, jugador):
        """
        Permite al jugador comprar una unidad.
        Muestra las opciones de unidades disponibles y realiza la compra si el jugador tiene suficientes monedas.
        """
        opciones = {
            "1": Soldado(),
            "2": Arquero(),
            "3": Caballero()
        }

        print("Elige la unidad que deseas comprar:")
        print("1) Soldado (coste: 5 monedas)")
        print("2) Arquero (coste: 6 monedas)")
        print("3) Caballero (coste: 9 monedas)")
        opcion = input("Introduce el número de opción: ")

        if opcion in opciones:
            unidad = opciones[opcion]
            costo = unidad.coste

            if jugador.get_monedas() >= costo:
                jugador.restar_monedas(costo)
                jugador.unidades.append(unidad)
                print(f"{jugador.nombre} ha comprado una unidad {type(unidad).__name__}.")
            else:
                print("No tienes suficientes monedas para comprar esta unidad.")
        else:
            print("Opción inválida. Por favor, elige una opción válida.")
        

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
        # Realizar el ataque de cada unidad del atacante al defensor
        for unidad in atacante.unidades:
            # Calcular puntos de ataque de la unidad y reducir los puntos de vida del defensor
            puntos_ataque = unidad.atacar(defensor)
            defensor.recibir_daño(puntos_ataque)

        # Verificar si el defensor se queda sin puntos de vida y finalizar el juego si es el caso
        if defensor.puntos_vida <= 0:
            self._finalizar(atacante)

        

    @staticmethod
    def _calcular_bonus(atacante, defensor):
        """Devuelve el bonus de ataque que tiene el atacante contra el defensor, se debe usar
         la función isinstace(instancia, clase) para implementarla"""
        
        if isinstance(atacante, Soldado) and isinstance(defensor, Arquero):
            return BONUS_DANO
        elif isinstance(atacante, Arquero) and isinstance(defensor, Caballero):
            return BONUS_DANO
        elif isinstance(atacante, Caballero) and isinstance(defensor, Soldado):
            return BONUS_DANO
        else:
            return 1.0
        
    def _batalla(self):
        """Realiza una batalla entre las unidades del jugador1 y el jugador2. 
        La batalla se desarrolla en combates 1 vs 1, siempre entre las unidades más antiguas de cada jugador.
        Durante un combate, las dos unidades pierdan tantos puntos de vida como puntos de ataque tenga la unidad adversaria.
        Si una unidad sobrevive a un combate, ésta participará en el siguiente combate, la batalla continua mientras ambos jugadores
         tengan unidades disponibles. 
        Cuando a un jugador no le queden más unidades, recibe un ataque de cada unidad enemiga remaniente.
        Al acabar, los jugadores hacen descansar a sus unidades.
        """

        while self.jugador1.unidades and self.jugador2.unidades:
            # Realizar batalla entre las unidades de los jugadores
            # Seleccionar la primera unidad de cada jugador
            unidad1 = self.jugador1.unidades.pop(0)
            unidad2 = self.jugador2.unidades.pop(0)

            # Calcular puntos de ataque de cada unidad teniendo en cuenta el bonus de ataque
            puntos_ataque1 = int(unidad1.atacar(unidad2) * self._calcular_bonus(unidad1, unidad2))
            puntos_ataque2 = int(unidad2.atacar(unidad1) * self._calcular_bonus(unidad2, unidad1))

            # Reducir los puntos de vida de los jugadores según los puntos de ataque de las unidades
            self.jugador1.puntos_vida -= puntos_ataque2
            self.jugador2.puntos_vida -= puntos_ataque1

            # Verificar si alguno de los jugadores se queda sin puntos de vida y finalizar el juego si es el caso
            if self.jugador1.puntos_vida <= 0:
                self._finalizar(self.jugador2)
            elif self.jugador2.puntos_vida <= 0:
                self._finalizar(self.jugador1)

        # Ataque adicional de las unidades restantes a los jugadores
        for unidad in self.jugador1.unidades + self.jugador2.unidades:
            # Calcular puntos de ataque de la unidad a ambos jugadores
            puntos_ataque = unidad.atacar(self.jugador1) + unidad.atacar(self.jugador2)

            # Reducir los puntos de vida de los jugadores según los puntos de ataque de la unidad
            self.jugador1.puntos_vida -= puntos_ataque
            self.jugador2.puntos_vida -= puntos_ataque

        # Hacer descansar a las unidades de ambos jugadores
        self.jugador1.descansar()
        self.jugador2.descansar()


        

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
