import sys
import pytest
from juego import Juego, N_VIDAS
from unidad import MAX_VIDA, Arquero, Caballero, Soldado, Unidad
from jugador import Jugador
from os import path
import shutil

import filecmp

"""
Cuando esta constante es true, substituirá los outputs de los tests de funcionalidad
por los actuales y ara fallar los tests hasta que se cambie de nuevo
"""
CREAR_OUTPUTS_FUNCIONALIDAD = False


class Test_unitarios():
    def test_crear_jugador(self):
        mi_jugador = Jugador("Bobby Fischer")
        mi_jugador.get_monedas()
        assert(mi_jugador.nombre == "Bobby Fischer")
        assert(mi_jugador.unidades == [])
        assert(mi_jugador.puntos_vida > 0)

    def test_monedas_negativas_jugador(self):
        mi_jugador = Jugador("José Raúl Capablanca")
        mi_jugador.set_monedas(-1)
        assert mi_jugador.get_monedas() == 0

    def test_crear_caballero(self):
        mi_caballero = Caballero()
        with pytest.raises(AttributeError):
            mi_caballero.preparado

    def test_herencia(self):
        assert(issubclass(Soldado, Unidad))
        assert(issubclass(Arquero, Unidad))
        assert(issubclass(Caballero, Unidad))

    def test_abstract_class(self):
        with pytest.raises(TypeError):
            mi_unidad = Unidad()

    def test_ataque_arquero(self):
        mi_arquero = Arquero()
        assert(mi_arquero.atacar() == 0)
        assert(mi_arquero.atacar() > 0)
        assert(mi_arquero.atacar() == 0)
        assert(mi_arquero.atacar() > 0)

    def test_ataque_soldado(self):
        mi_soldado = Soldado()
        assert(mi_soldado.atacar() > 0)

    def test_descansar_soldado(self):
        mi_soldado = Soldado()
        max_puntos_vida = mi_soldado.puntos_vida
        mi_soldado.puntos_vida -= 1
        mi_soldado.descansar()

        assert(max_puntos_vida == mi_soldado.puntos_vida)

    def test_bonus(self):
        miJuego = Juego("Jugador1", "Jugador2")
        miSoldado = Soldado()
        miArquero = Arquero()
        miCaballero = Caballero()

        assert(miJuego._calcular_bonus(miSoldado, miArquero) == 1.5)
        assert(miJuego._calcular_bonus(miArquero, miCaballero) == 1.5)
        assert(miJuego._calcular_bonus(miCaballero, miSoldado) == 1.5)
        assert(miJuego._calcular_bonus(miArquero, miSoldado) == 1)
        assert(miJuego._calcular_bonus(miCaballero, miCaballero) == 1)


class Test_integracion():

    def test_arquero_daño_jugador(self):
        miJuego = Juego("Jugador1", "Jugador2")

        miJuego.jugador2.unidades.append(Arquero())

        miJuego._batalla()
        miJuego._batalla()

        assert(miJuego.jugador1.puntos_vida == 12)
        assert(miJuego.jugador2.puntos_vida == 20)

    def test_descansar_jugador(self):
        mi_jugador = Jugador("Garry Kasparov")
        mi_soldado = Soldado()
        max_puntos_vida = mi_soldado.puntos_vida
        mi_soldado.puntos_vida -= 1
        mi_jugador.unidades.append(mi_soldado)
        mi_jugador.descansar()

        assert(max_puntos_vida == mi_soldado.puntos_vida)

    def test_descansar_jugador_sin_unidades(self):
        mi_jugador = Jugador("Garry Kasparov")
        mi_soldado = Soldado()
        mi_jugador.descansar()

    def test_daño_al_jugador(self):
        miJuego = Juego("Jugador1", "Jugador2")
        miSoldado = Soldado()
        miJuego.jugador1.unidades.append(miSoldado)
        miJuego._daño_al_jugador(miJuego.jugador2, miJuego.jugador1)
        assert(N_VIDAS-miSoldado._puntos_ataque ==
               miJuego.jugador2.puntos_vida)

    def test_finalizar_partida_jugador(self):
        miJuego = Juego("Jugador1", "Jugador2")
        for i in range(100):
            miJuego.jugador1.unidades.append(Soldado())
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            miJuego._daño_al_jugador(
                miJuego.jugador2, miJuego.jugador1)

    def test_batalla_soldado_soldado(self):
        miJuego = Juego("Jugador1", "Jugador2")

        miSoldado = Soldado()
        miJuego.jugador1.unidades.append(miSoldado)

        miArquero = Soldado()
        miJuego.jugador2.unidades.append(miArquero)

        miJuego._batalla()
        assert(miJuego.jugador1.puntos_vida == 20)
        assert(miJuego.jugador2.puntos_vida == 20)

    def test_batalla_soldado_vs_arquero(self):
        miJuego = Juego("Jugador1", "Jugador2")

        miSoldado = Soldado()
        miJuego.jugador1.unidades.append(miSoldado)

        miArquero = Arquero()
        miJuego.jugador2.unidades.append(miArquero)

        miJuego._batalla()
        assert(miJuego.jugador1.puntos_vida == 20)
        assert(miJuego.jugador2.puntos_vida == 17)

    def test_batalla_soldado_vs_2_soldados(self):
        miJuego = Juego("Jugador1", "Jugador2")

        miJuego.jugador1.unidades.append(Soldado())

        miJuego.jugador2.unidades.append(Soldado())
        miJuego.jugador2.unidades.append(Soldado())

        miJuego._batalla()
        assert(miJuego.jugador1.puntos_vida == 17)
        assert(miJuego.jugador2.puntos_vida == 20)

    def test_batalla_soldado_vs_2_arqueros(self):
        miJuego = Juego("Jugador1", "Jugador2")

        miSoldado = Soldado()
        miJuego.jugador1.unidades.append(miSoldado)

        miJuego.jugador2.unidades.append(Arquero())
        miJuego.jugador2.unidades.append(Arquero())

        miJuego._batalla()
        assert(miJuego.jugador1.puntos_vida == 20)
        assert(miJuego.jugador2.puntos_vida == 20)


def check_same_output(path_orginial, path_test, create_output):
    """Devuelve true en caso de que los dos ficheros sean iguales, en caso de que create_output
    sea cierto copiar el output actual como el nuevo output a comparar, y hará fallar el test"""
    if create_output:
        shutil.copy(path_test, path_orginial)
        pytest.fail(f"Fichero {path_orginial} creado")
    assert(filecmp.cmp(path_orginial,
                       path_test, shallow=False))


class Test_funcionalidad():

    def test_comprar_soldado(self, monkeypatch):
        sol_file_path = 'test/test_comprar_soldado.out'
        test_path = 'test/test.out'
        with open('test/test.out', 'w', encoding="utf-8") as file:
            sys.stdout = file
            Juego.mensaje_bienvenida()
            juego = Juego("Jugador1", "jugador2")
            # Entrada ficticia de los jugadores
            answers = iter([3, 1])

            # using lambda statement for mocking
            monkeypatch.setattr('builtins.input', lambda name: next(answers))
            with pytest.raises(SystemExit) as e:
                juego.loop()
            assert e.type == SystemExit

        check_same_output(sol_file_path, test_path,
                          CREAR_OUTPUTS_FUNCIONALIDAD)

    def test_dinero_insuficiente(self, monkeypatch):
        sol_file_path = 'test/test_dinero_insuficiente.out'
        test_path = 'test/test.out'
        with open('test/test.out', 'w', encoding="utf-8") as file:
            sys.stdout = file
            Juego.mensaje_bienvenida()
            juego = Juego("Jugador1", "jugador2")
            # Entrada ficticia de los jugadores
            answers = iter([3, 3, 3, 1])

            # using lambda statement for mocking
            monkeypatch.setattr('builtins.input', lambda name: next(answers))
            with pytest.raises(SystemExit) as e:
                juego.loop()
            assert e.type == SystemExit

        check_same_output(sol_file_path, test_path,
                          CREAR_OUTPUTS_FUNCIONALIDAD)

    def test_comprar_dos_soldados(self, monkeypatch):
        sol_file_path = 'test/test_comprar_dos_soldados.out'
        test_path = 'test/test.out'
        with open(test_path, 'w', encoding="utf-8") as file:
            sys.stdout = file
            Juego.mensaje_bienvenida()
            juego = Juego("Jugador1", "jugador2")
            # Entrada ficticia de los jugadores
            answers = iter([3, 3, 1])

            # using lambda statement for mocking
            monkeypatch.setattr('builtins.input', lambda name: next(answers))
            with pytest.raises(SystemExit) as e:
                juego.loop()
            assert e.type == SystemExit

        check_same_output(sol_file_path, test_path,
                          CREAR_OUTPUTS_FUNCIONALIDAD)

    def test_jugador_1_gana_partida(self, monkeypatch):
        sol_file_path = 'test/test_jugador_1_gana_partida.out'
        test_path = 'test/test.out'
        with open(test_path, 'w', encoding="utf-8") as file:
            sys.stdout = file
            Juego.mensaje_bienvenida()
            juego = Juego("Jugador1", "jugador2")
            # Entrada ficticia de los jugadores
            answers = iter([3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2])

            # using lambda statement for mocking
            monkeypatch.setattr('builtins.input', lambda name: next(answers))
            with pytest.raises(SystemExit) as pytest_wrapped_e:
                juego.loop()
            assert pytest_wrapped_e.type == SystemExit

        check_same_output(sol_file_path, test_path,
                          CREAR_OUTPUTS_FUNCIONALIDAD)

    def test_jugador_2_gana_partida(self, monkeypatch):

        sol_file_path = 'test/test_jugador_2_gana_partida.out'
        test_path = 'test/test.out'
        with open(test_path, 'w', encoding="utf-8") as file:
            sys.stdout = file
            Juego.mensaje_bienvenida()
            juego = Juego("Jugador1", "jugador2")
            # Entrada ficticia de los jugadores
            answers = iter([2, 4, 4, 2, 2, 4, 4, 2, 2, 4, 4, 2, 2, 4, 4, 2])

            # using lambda statement for mocking
            monkeypatch.setattr('builtins.input', lambda name: next(answers))

            with pytest.raises(SystemExit) as pytest_wrapped_e:
                juego.loop()
            assert pytest_wrapped_e.type == SystemExit

        check_same_output(sol_file_path, test_path,
                          CREAR_OUTPUTS_FUNCIONALIDAD)

    def test_final(self, monkeypatch):

        sol_file_path = 'test/test_final.out'
        test_path = 'test/test.out'
        with open(test_path, 'w', encoding="utf-8") as file:
            sys.stdout = file
            Juego.mensaje_bienvenida()
            juego = Juego("Jugador1", "jugador2")
            # Entrada ficticia de los jugadores
            answers = iter([3, 3, 2, 5, 2, 4, 2, 5, 2, 5, 3, 4, 2, 3, 3, 2, 1])

            # using lambda statement for mocking
            monkeypatch.setattr('builtins.input', lambda name: next(answers))
            with pytest.raises(SystemExit) as e:
                juego.loop()
            assert e.type == SystemExit

        check_same_output(sol_file_path, test_path,
                          CREAR_OUTPUTS_FUNCIONALIDAD)


class Test_usuario():
    def test_integracion_a_implementar(self):
        # Eliminar la siguiente linea
        assert(False)

    def test_unitario_a_implementar(self):
        # Eliminar la siguiente linea
        assert(False)

    def test_funcional_a_implementar(self):
        # Eliminar la siguiente linea
        assert(False)
