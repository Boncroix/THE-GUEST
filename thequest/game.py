import pygame as pg

from . import ALTO, ANCHO, DIFICULTAD_INI, VIDAS
from .escenas import Partida, Portada, Records


class TheQuest:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('The  Quest')
        self.dificultad = DIFICULTAD_INI
        self.vidas = VIDAS
        self.puntos = 0

    def jugar(self):
        escena_selec = 'portada'
        while True:
            self.escenas = {
                'portada': Portada(self.pantalla),
                'partida': Partida(self.pantalla, self.dificultad, self.vidas, self.puntos),
                'records': Records(self.pantalla)
            }

            if escena_selec == 'salir':
                print('La escena me pide que acabe el juego')
                break
            elif escena_selec == 'partida':
                escena_selec, self.dificultad, self.vidas, self.puntos = self.escenas[escena_selec].bucle_principal(
                )
                print('La escena PARTIDA me pide que cambie de escena')
            else:
                escena_selec = self.escenas[escena_selec].bucle_principal()
                print('La escena me pide que cambie de escena')

            pg.mixer.music.stop()

        pg.quit()
