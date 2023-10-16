import os

import pygame as pg

from .import ALTO, ANCHO, VELOCIDAD_NAVE


class Nave(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(3):
            ruta_image = os.path.join(
                'resources', 'images', f'nave{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))

        self.contador = 0
        self.image = self.imagenes[self.contador]

        self.rect = self.image.get_rect(midleft=(0, ALTO / 2))

    def update(self):
        self.contador += 1
        if self.contador > 2:
            self.contador = 0
        self.image = self.imagenes[self.contador]

        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_a]:
            self.rect.y -= VELOCIDAD_NAVE
            if self.rect.top < 0:
                self.rect.top = 0

        if estado_teclas[pg.K_z]:
            self.rect.y += VELOCIDAD_NAVE
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO
