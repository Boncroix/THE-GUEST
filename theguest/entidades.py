import os

import pygame as pg

from random import choice, randint

from theguest.dbmanager import DBManager

from .import (ALTO, ANCHO, CENTRO_X, CENTRO_Y, COLORES, DIFICULTAD_INI, DISPAROS_POR_NIVEL,
              FUENTES, MARGEN_IZQ, MARGEN_INF, MARGEN_SUP, NIVEL_CON_HABILIDADES, NIVEL_INI,
              TAM_FUENTE, VIDAS_INI
              )


class Nave(pg.sprite.Sprite):
    aumento_vel_nave = 1
    vel_nave = 5
    angulo_destino = 180
    vel_aterrizaje = 2
    habilitar_mov_der_izq = False

    def __init__(self):
        super().__init__()
        self.velocidad_up = self.velocidad_dow = self.velocidad_right = self.velocidad_left = self.vel_nave
        self.imagenes = []
        for i in range(4):
            ruta_image = os.path.join(
                'resources', 'images', f'nave{i}.png')
            self.imagenes.append(pg.image.load(ruta_image))
        self.contador = 0
        self.image = self.imagenes[self.contador]
        self.rect = self.image.get_rect(
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
        elif estado_teclas[pg.K_LEFT] and not estado_teclas[pg.K_RIGHT] and self.habilitar_mov_der_izq:
            self.velocidad_right = self.vel_nave
            self.rect.x -= self.velocidad_left
            self.velocidad_left += self.aumento_vel_nave
            if self.rect.left < 0:
                self.rect.left = 0
        elif estado_teclas[pg.K_RIGHT] and not estado_teclas[pg.K_LEFT] and self.habilitar_mov_der_izq:
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

        if self.rect.right < planeta.rect.left + self.rect.width * 2/20:
            self.rect.x += self.vel_aterrizaje
        if self.rect.centery > CENTRO_Y:
            self.rect.y -= self.vel_aterrizaje
        if self.rect.centery < CENTRO_Y:
            self.rect.y += self.vel_aterrizaje

        if self.angulo_rotacion < self.angulo_destino:
            self.image = pg.transform.rotate(
                self.image_original, self.angulo_rotacion)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.angulo_rotacion += 1


class Nave1(Nave):
    habilitar_mov_der_izq = True

    def __init__(self):
        super().__init__()


class Proyectil(pg.sprite.Sprite):
    vel_proyectil = 10

    def __init__(self, nave):
        super().__init__()
        self.nave = nave
        ruta_image = os.path.join('resources', 'images', 'disparo.png')
        self.image = pg.image.load(ruta_image)
        self.rect = self.image.get_rect(midleft=(self.nave.rect.midright))

    def update(self, proyectil):
        self.rect.left += self.vel_proyectil
        if self.rect.right > ANCHO:
            proyectil.remove(self)


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

    def update(self, obstaculo):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            obstaculo.remove(self)
            return True
        return False


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


class IndicadorDisparo(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ruta_image = os.path.join('resources', 'images', 'disparo.png')
        self.image = pg.image.load(ruta_image)
        self.rect = self.image.get_rect()


class Planeta(pg.sprite.Sprite):
    vel_planeta = 2

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


class Marcador:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.tipo3 = pg.font.Font(FUENTES['nasa'], TAM_FUENTE['3'])
        self.db = DBManager()
        self.crear_disparos(DISPAROS_POR_NIVEL)

    def reset(self):
        self.vidas = VIDAS_INI
        self.puntos = 0
        self.nivel = NIVEL_INI
        self.dificultad = DIFICULTAD_INI + self.nivel
        self.crear_vidas(self.vidas)
        self.crear_disparos(DISPAROS_POR_NIVEL)

    def incrementar_puntos(self, puntos):
        self.puntos += puntos

    def restar_vida(self):
        self.vidas -= 1
        self.crear_vidas(self.vidas)
        self.crear_disparos(DISPAROS_POR_NIVEL)

    def restar_disparo(self):
        self.disparos -= 1
        self.indicador_disparo.sprites()[-1].kill()

    def subir_nivel(self):
        self.nivel += 1
        self.dificultad += 1
        self.crear_disparos(DISPAROS_POR_NIVEL)

    def pintar(self):
        # Pintar Puntos
        self.pintar_texto([str(self.puntos),], self.tipo3, MARGEN_IZQ,
                          0, '', COLORES['blanco'])
        # Pintar Nivel
        self.pintar_texto(['Nivel ' + str(self.nivel),], self.tipo3, ANCHO * 4/5,
                          0, '', COLORES['blanco'])
        # Pintar mejor jugador
        self.consultar_max_records()

        self.pintar_texto(['High Score   ' + str(self.max_records),], self.tipo3, CENTRO_X,
                          MARGEN_INF, '', COLORES['blanco'])

        self.indicador_vidas.update()
        self.indicador_vidas.draw(self.pantalla)
        if self.nivel > NIVEL_CON_HABILIDADES:
            self.indicador_disparo.draw(self.pantalla)

    def pintar_texto(self, mensaje, tipo, pos_x, pos_y, alineacion, color):
        for linea in mensaje:
            linea = str(linea)
            if '\n' in linea:
                linea = linea[:-1]
            texto = tipo.render(linea, True, color)
            if alineacion == 'centro':
                pos_x_centro = pos_x - (texto.get_width() / 2)
                self.pantalla.blit(texto, (pos_x_centro, pos_y))
            elif alineacion == 'derecha':
                pos_x_centro = pos_x - texto.get_width()
                self.pantalla.blit(texto, (pos_x_centro, pos_y))
            else:
                self.pantalla.blit(texto, (pos_x, pos_y))
            pos_y += texto.get_height()

    def consultar_max_records(self):
        sql = 'SELECT puntos FROM records ORDER BY puntos DESC, id ASC'
        self.records = self.db.consultaSQL(sql)
        self.max_records = self.records[0][0]
        if self.puntos > self.max_records:
            self.max_records = self.puntos

    def crear_vidas(self, vidas):
        self.indicador_vidas = pg.sprite.Group()
        for vida in range(vidas):
            indicador = IndicadorVida()
            separador = indicador.rect.width / 2
            indicador.rect.center = (indicador.rect.width * vida + MARGEN_IZQ + separador * vida + indicador.rect.width / 2,
                                     ALTO - (ALTO - MARGEN_INF) / 2)
            self.indicador_vidas.add(indicador)

    def crear_disparos(self, disparos):
        self.disparos = disparos
        self.indicador_disparo = pg.sprite.Group()
        for disparo in range(disparos):
            indicador = IndicadorDisparo()
            separador = indicador.rect.width / 2
            indicador.rect.center = (indicador.rect.width * disparo + ANCHO * 1/3 + separador * disparo,
                                     ALTO - (ALTO - MARGEN_INF) / 2)
            self.indicador_disparo.add(indicador)
