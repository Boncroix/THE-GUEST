import pygame as pg

from . import ALTO, ANCHO
from .escenas import Partida, Portada, Records


class TheQuest:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))

    def jugar(self):
        salir = False
        while not salir:

            self.escenas = [
                Portada(self.pantalla),
                Partida(self.pantalla),
                Records(self.pantalla)
            ]

            for escena in self.escenas:
                termine = escena.bucle_principal()
                if termine:
                    break

        pg.quit()
