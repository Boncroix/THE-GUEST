import os

import pygame as pg

from random import choice, randint
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


class Obstaculo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocidad = randint(5, 10)
        self.imagenes = []
        for i in range(5):
            ruta_image = os.path.join(
                'resources', 'images', f'obstaculo{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))

        pos_x = ANCHO + randint(MARGEN_Y, ANCHO)
        pos_y = randint(0, ALTO)
        self.image = choice(self.imagenes)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        if self.rect.top < MARGEN_Y:
            self.rect.top = MARGEN_Y
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

    def update(self, obstaculos):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            print('paso por auí')
            obstaculos.remove(self)
