import pygame as pg

from theguest.escenas.sc_portada import Portada
from theguest.escenas.sc_records import Records
from theguest.escenas.sc_partida import Partida

from . import ALTO, ANCHO, DIFICULTAD_INI, MUSICA, VIDAS


class TheGuest:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('The  Quest')
        self.sonido_activo = False

    def jugar(self):
        self.escena_selec = 'portada'
        while True:
            if self.escena_selec == 'portada':
                self.dificultad = DIFICULTAD_INI
                self.vidas = VIDAS
                self.puntos = 0
                self.nivel = 1
                self.musica = pg.mixer.music.load(MUSICA['portada'])
                self.musica = pg.mixer.music.play(-1)
                self.escena = Portada(self.pantalla, self.sonido_activo)
                self.escena_selec, self.sonido_activo = self.escena.bucle_principal(
                )
                self.musica = pg.mixer.music.load(MUSICA['partida'])
                self.musica = pg.mixer.music.play(-1)
            elif self.escena_selec == 'partida':
                self.escena = Partida(self.pantalla, self.dificultad,
                                      self.vidas, self.puntos, self.nivel, self.sonido_activo)
                self.escena_selec, self.dificultad, self.vidas, self.puntos, self.nivel, self.sonido_activo = self.escena.bucle_principal(
                )
            elif self.escena_selec == 'records':
                self.musica = pg.mixer.music.load(MUSICA['records'])
                self.musica = pg.mixer.music.play(-1)
                self.escena = Records(
                    self.pantalla, self.sonido_activo, self.puntos)
                self.escena_selec, self.sonido_activo, self.puntos = self.escena.bucle_principal(
                )
            elif self.escena_selec == 'salir':
                pg.mixer.music.stop()
                break

        pg.quit()
