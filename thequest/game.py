import pygame as pg

from . import ALTO, ANCHO
from .escenas import Partida, Portada, Records


class TheQuest:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('The  Quest')

    def jugar(self):
        salir = False
        while not salir:
            self.escenas = [
                Portada(self.pantalla),
                Partida(self.pantalla),
                Records(self.pantalla)
            ]

            for escena in self.escenas:
                he_acabado = escena.bucle_principal()
                if he_acabado:
                    print('La escena me pide que acabe el juego')
                    break
            salir = True
        print('He salido del bucle for de las escenas')

        pg.quit()
