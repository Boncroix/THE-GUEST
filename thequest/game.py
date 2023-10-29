import pygame as pg

from . import ALTO, ANCHO, DIFICULTAD_INI, MUSICA, VIDAS
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
        self.nivel = 1
        self.sonido_activo = False

    def jugar(self):
        self.escena_selec = 'portada'

        while True:
            self.escenas = {
                'portada': Portada(self.pantalla, self.sonido_activo),
                'partida': Partida(self.pantalla, self.dificultad, self.vidas, self.puntos, self.nivel, self.sonido_activo),
                'records': Records(self.pantalla, self.sonido_activo)
            }
            if self.escena_selec == 'portada':
                self.musica = pg.mixer.music.load(MUSICA['portada'])
                self.musica = pg.mixer.music.play(-1)
                self.escena_selec, self.sonido_activo = self.escenas[self.escena_selec].bucle_principal(
                )
                self.musica = pg.mixer.music.load(MUSICA['partida'])
                self.musica = pg.mixer.music.play(-1)
            elif self.escena_selec == 'partida':
                self.escena_selec, self.dificultad, self.vidas, self.puntos, self.nivel, self.sonido_activo = self.escenas[self.escena_selec].bucle_principal(
                )
            elif self.escena_selec == 'records':
                self.musica = pg.mixer.music.load(MUSICA['records'])
                self.musica = pg.mixer.music.play(-1)
                self.escena_selec, self.sonido_activo = self.escenas[self.escena_selec].bucle_principal(
                )
            elif self.escena_selec == 'salir':
                break

        pg.quit()

    def seleccionar_musica(self):
        if self.escena_selec == 'partida':
            pass
