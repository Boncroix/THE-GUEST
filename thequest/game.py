import pygame as pg

from thequest.entidades import Marcador

from thequest.escenas.sc_portada import Portada
from thequest.escenas.sc_records import Records
from thequest.escenas.sc_partida import Partida

from . import ALTO, ANCHO, MUSICA


class TheQuest:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('The  Quest')
        self.sonido_activo = True
        self.musica = pg.mixer.music.load(MUSICA['records'])
        self.musica = pg.mixer.music.play(-1)
        self.marcador = Marcador(self.pantalla)

    def jugar(self):
        self.escena_selec = 'portada'
        while True:
            if self.escena_selec == 'portada':
                self.marcador.reset()
                self.escena = Portada(self.pantalla, self.sonido_activo)
                self.escena_selec, self.sonido_activo = self.escena.bucle_principal(
                )
                if self.escena_selec == 'partida':
                    self.musica = pg.mixer.music.load(MUSICA['partida'])
                    self.musica = pg.mixer.music.play(-1)

            elif self.escena_selec == 'partida':
                self.escena = Partida(self.pantalla, self.sonido_activo, self.marcador)
                self.escena_selec, self.sonido_activo = self.escena.bucle_principal(
                )
                if self.escena_selec == 'records':
                    self.musica = pg.mixer.music.load(MUSICA['records'])
                    self.musica = pg.mixer.music.play(-1)

            elif self.escena_selec == 'records':
                self.escena = Records(
                    self.pantalla, self.sonido_activo, self.marcador)
                self.escena_selec, self.sonido_activo = self.escena.bucle_principal(
                )
            elif self.escena_selec == 'salir':
                pg.mixer.music.stop()
                break

        pg.quit()
