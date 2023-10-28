import os

import pygame as pg
import math

from random import choice, randint

from .import (ALTO, ANCHO, CENTRO_X, CENTRO_Y, HABILITAR_MOV_DER_IZQ,
              MARGEN_IZQ, MARGEN_INF, MARGEN_SUP
              )


class Nave(pg.sprite.Sprite):
    aumento_vel_nave = 1
    vel_nave = 5
    angulo_destino = 180

    def __init__(self):
        super().__init__()
        self.velocidad_up = self.velocidad_dow = self.velocidad_right = self.velocidad_left = self.vel_nave
        self.imagenes = []
        for i in range(4):
            ruta_image = os.path.join(
                'resources', 'images', f'nave{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))
        self.contador = 0
        self.image = self.image_original = self.imagenes[self.contador]
        self.rect = self.rect_original = self.image.get_rect(
            midleft=(0, CENTRO_Y))
        self.angulo_rotacion = 0

    def update(self):
        if self.contador == len(self.imagenes) - 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]
        self.contador += 1

        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_UP] and not estado_teclas[pg.K_DOWN]:
            self.velocidad_dow = self.vel_nave
            self.rect.y -= self.velocidad_up
            self.velocidad_up += self.aumento_vel_nave
            if self.rect.top < MARGEN_SUP:
                self.rect.top = MARGEN_SUP
        elif estado_teclas[pg.K_DOWN] and not estado_teclas[pg.K_UP]:
            self.velocidad_up = self.vel_nave
            self.rect.y += self.velocidad_dow
            self.velocidad_dow += self.aumento_vel_nave
            if self.rect.bottom > MARGEN_INF:
                self.rect.bottom = MARGEN_INF
        elif estado_teclas[pg.K_LEFT] and not estado_teclas[pg.K_RIGHT] and HABILITAR_MOV_DER_IZQ:
            self.velocidad_right = self.vel_nave
            self.rect.x -= self.velocidad_left
            self.velocidad_left += self.aumento_vel_nave
            if self.rect.left < 0:
                self.rect.left = 0
        elif estado_teclas[pg.K_RIGHT] and not estado_teclas[pg.K_LEFT] and HABILITAR_MOV_DER_IZQ:
            self.velocidad_left = self.vel_nave
            self.rect.x += self.velocidad_right
            self.velocidad_right += self.aumento_vel_nave
            if self.rect.right > CENTRO_X:
                self.rect.right = CENTRO_X
        else:
            self.velocidad_up = self.velocidad_dow = self.velocidad_right = self.velocidad_left = self.vel_nave

    def explosion_nave(self):
        self.image = self.imagenes[-1]

    def aterrizar_nave(self, planeta):
        if self.contador == len(self.imagenes) - 1:
            self.contador = 0
        self.image_original = self.image = self.imagenes[self.contador]
        self.image = pg.transform.rotate(self.image, self.angulo_rotacion)
        self.contador += 1

        # FIXME Preguntar por la velocidadd de la nave aterrizando si tiene que ser constante
        if planeta.planeta_posicionado:
            if self.rect.right < planeta.rect.left + self.rect.width * 2/20:
                self.rect.x += 1
            if self.rect.centery > CENTRO_Y:
                self.rect.y -= 1
            if self.rect.centery < CENTRO_Y:
                self.rect.y += 1

            if self.angulo_rotacion < self.angulo_destino:
                self.image = pg.transform.rotate(
                    self.image_original, self.angulo_rotacion)
                self.rect = self.image.get_rect(center=self.rect.center)
                self.angulo_rotacion += 1


class Disparo(pg.sprite.Sprite):
    # TODO Generar disparo de la nave
    pass


class Obstaculo(pg.sprite.Sprite):
    puntos_por_obstaculo = 20

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
            return self.puntos_por_obstaculo
        return 0


class IndicadorVida(pg.sprite.Sprite):
    escala_x_ini_vidas = 70
    escala_y_ini_vidas = 40

    def __init__(self):
        super().__init__()
        self.imagenes = []
        for i in range(3):
            ruta_image = os.path.join(
                'resources', 'images', f'nave{i}.png')
            self.image = pg.image.load(ruta_image)
            self.image = pg.transform.scale(
                self.image, (self.escala_x_ini_vidas, self.escala_y_ini_vidas))
            self.imagenes.append(self.image)

        self.contador = 0
        self.rect = self.image.get_rect()
        self.image = self.imagenes[self.contador]

    def update(self):
        self.contador += 1
        if self.contador > len(self.imagenes) - 1:
            self.contador = 0
        self.image = self.imagenes[self.contador]


class Planeta(pg.sprite.Sprite):
    vel_planeta = 5

    def __init__(self):
        super().__init__()
        ruta_image = os.path.join('resources', 'images', 'planeta.png')
        self.image = pg.image.load(ruta_image)
        self.rect = self.image.get_rect(midleft=(ANCHO, CENTRO_Y))
        self.planeta_posicionado = False

    def update(self):
        self.rect.left -= self.vel_planeta
        if self.rect.left <= ANCHO * 3/4:
            self.rect.left = ANCHO * 3/4
            self.planeta_posicionado = True
