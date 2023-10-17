import os

import pygame as pg

from random import randint
from .import ALTO, ANCHO, AUMENTO_VELOCIDAD_NAVE, MARGEN_Y, VELOCIDAD_NAVE


class Nave(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.velocidad_up = VELOCIDAD_NAVE
        self.velocidad_dow = VELOCIDAD_NAVE
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
            self.velocidad_dow = VELOCIDAD_NAVE
            self.rect.y -= self.velocidad_up
            self.velocidad_up += AUMENTO_VELOCIDAD_NAVE
            if self.rect.top < MARGEN_Y:
                self.rect.top = MARGEN_Y

        if estado_teclas[pg.K_z]:
            self.velocidad_up = VELOCIDAD_NAVE
            self.rect.y += self.velocidad_dow
            self.velocidad_dow += AUMENTO_VELOCIDAD_NAVE
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO


class Obstaculos(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.imagenes = []
        for i in range(8):
            ruta_image = os.path.join(
                'resources', 'images', f'objeto{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))

    def crear_obstaculo(self):
        self.image = self.imagenes[randint(0, 7)]
        self.rect = self.image.get_rect(
            midright=(ANCHO + 700, randint(0, ALTO)))
