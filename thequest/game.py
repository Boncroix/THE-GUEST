import pygame as pg

from . import ALTO, ANCHO
from .escenas import Partida, Portada, Records


class TheQuest:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('The  Quest')

    def jugar(self):
        escena_selec = 'portada'
        while True:
            self.escenas = {
                'portada': Portada(self.pantalla),
                'partida': Partida(self.pantalla),
                'records': Records(self.pantalla)
            }

            if escena_selec == 'salir':
                print('La escena me pide que acabe el juego')
                break
            else:
                escena_selec = self.escenas[escena_selec].bucle_principal()
                print('La escena me pide que cambie de escena')
            pg.mixer.music.stop()

        pg.quit()
