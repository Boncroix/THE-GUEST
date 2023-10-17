import os


import pygame as pg


from .import (ALTO, ANCHO, AZUL, BLANCO, CENTRO_X, CENTRO_Y, FPS, HISTORIA, INFO, INSTRUCCIONES,
              INTERVALO_PARPADEO_INFO, MARGEN_X, FUENTE_NASA, FUENTE_CONTRAST,
              ROJO, TAM_FUENTE_1, TAM_FUENTE_2, TAM_FUENTE_3, TAM_FUENTE_4,
              VELOCIDAD_FONDO_PARTIDA, VERDE)

from .entidades import Nave




    def pintar_portada(self):
        estado_teclas = pg.key.get_pressed()
        # MOSTRAR TITULO
        self.pintar_texto(['THE QUEST ',], self.tipo4, CENTRO_X,
                          ALTO * 17/20, 'centro', VERDE, True)
        # MOSTRAR INFORMACIÓN
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio >= INTERVALO_PARPADEO_INFO:
            self.parpadeo_visible = not self.parpadeo_visible
            self.ultimo_cambio = tiempo_actual
        if self.parpadeo_visible:
            self.pintar_texto(INFO, self.tipo3, CENTRO_X,
                              0, 'centro', BLANCO, False)
        # MOSTRAR HISTORIA
        self.pintar_texto(HISTORIA, self.tipo2, CENTRO_X,
                          ALTO * 11/20, 'centro', BLANCO, False)
        # MOSTRAR INSTRUCCIONES
        if estado_teclas[pg.K_i]:
            self.pintar_texto(INSTRUCCIONES, self.tipo2, MARGEN_X,
                              ALTO * 7/20, '', BLANCO, True)
        # MOSTRAR RECORDS
        if estado_teclas[pg.K_r]:
            self.pantalla.blit(self.image, (0, 0))

    def pintar_texto(self, txt, tipo, pos_x, pos_y, alineacion, color, fondo):
        if fondo == True:
            self.pantalla.blit(self.image, (0, 0))
        for linea in txt:
            texto = tipo.render(linea[:-1], True, color)
            if alineacion == 'centro':
                pos_x_centro = pos_x - (texto.get_width() / 2)
                self.pantalla.blit(texto, (pos_x_centro, pos_y))
            elif alineacion == 'derecha':
                pos_x_centro = pos_x - texto.get_width()
                self.pantalla.blit(texto, (pos_x_centro, pos_y))
            else:
                self.pantalla.blit(texto, (pos_x, pos_y))
            pos_y += texto.get_height()
