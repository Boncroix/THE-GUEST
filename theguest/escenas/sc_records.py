import os

import pygame as pg

from theguest import (ALTO, ANCHO, IMAGENES)

from .sc_escena import Escena


class Records(Escena):
    def __init__(self, pantalla, sonido_activo):
        super().__init__(pantalla)
        self.sonido_activo = sonido_activo
        self.image = pg.image.load(IMAGENES['records']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena records')
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_s:
                    self.sonido_activo = not self.sonido_activo
            self.pantalla.blit(self.image, (0, 0))
            self.comprobar_sonido()
            pg.display.flip()
