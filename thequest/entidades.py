import os

import pygame as pg

from random import choice, randint

from .import (ALTO, ANCHO, AUMENTO_VEL_NAVE, CENTRO_Y, ESCALA_X_INDI_VIDAS, ESCALA_Y_INDI_VIDAS, HABILITAR_MOV_DER_IZQ,
              MARGEN_IZQ, MARGEN_INF, MARGEN_SUP, VEL_NAVE
              )


class Nave(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.velocidad_up = self.velocidad_dow = self.velocidad_right = self.velocidad_left = VEL_NAVE
        self.imagenes = []
        for i in range(4):
            ruta_image = os.path.join(
                'resources', 'images', f'nave{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))
        self.contador = 0
        self.image = self.imagenes[self.contador]
        self.rect = self.image.get_rect(midleft=(0, CENTRO_Y))

    def update(self):
        if self.contador == len(self.imagenes) - 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]
        self.contador += 1

        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_UP]:
            self.velocidad_dow = VEL_NAVE
            self.rect.y -= self.velocidad_up
            self.velocidad_up += AUMENTO_VEL_NAVE
            if self.rect.top < MARGEN_SUP:
                self.rect.top = MARGEN_SUP

        if estado_teclas[pg.K_DOWN]:
            self.velocidad_up = VEL_NAVE
            self.rect.y += self.velocidad_dow
            self.velocidad_dow += AUMENTO_VEL_NAVE
            if self.rect.bottom > MARGEN_INF:
                self.rect.bottom = MARGEN_INF

        if HABILITAR_MOV_DER_IZQ:
            if estado_teclas[pg.K_LEFT]:
                self.velocidad_right = VEL_NAVE
                self.rect.x -= self.velocidad_left
                self.velocidad_left += AUMENTO_VEL_NAVE
                if self.rect.left < 0:
                    self.rect.left = 0

            if estado_teclas[pg.K_RIGHT]:
                self.velocidad_left = VEL_NAVE
                self.rect.x += self.velocidad_right
                self.velocidad_right += AUMENTO_VEL_NAVE
                if self.rect.right > ANCHO:
                    self.rect.right = ANCHO

    def explosion_nave(self):
        self.image = self.imagenes[-1]


class Disparo(pg.sprite.Sprite):
    # TODO Generar disparo de la nave
    pass


class Obstaculo(pg.sprite.Sprite):

    def __init__(self, aumento_vel):
        super().__init__()
        self.velocidad = randint(
            aumento_vel, aumento_vel * 2)
        self.imagenes = []
        for i in range(6):
            ruta_image = os.path.join(
                'resources', 'images', f'obstaculo{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))

        pos_x = ANCHO + randint(MARGEN_IZQ, ANCHO)
        pos_y = randint(MARGEN_SUP, MARGEN_INF)
        self.image = choice(self.imagenes)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        if self.rect.top < MARGEN_SUP:
            self.rect.top = MARGEN_SUP
        if self.rect.bottom > MARGEN_INF:
            self.rect.bottom = MARGEN_INF

    def update(self, obstaculos):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            obstaculos.remove(self)
            return 20
        return 0


class IndicadorVida(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(3):
            ruta_image = os.path.join(
                'resources', 'images', f'nave{i}.png')
            self.image = pg.image.load(ruta_image)
            self.image = pg.transform.scale(
                self.image, (ESCALA_X_INDI_VIDAS, ESCALA_Y_INDI_VIDAS))
            self.imagenes.append(self.image)

        self.contador = 0
        self.rect = self.image.get_rect()
        self.image = self.imagenes[self.contador]

    def update(self):
        self.contador += 1
        if self.contador > len(self.imagenes) - 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]
