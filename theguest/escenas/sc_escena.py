import os

import pygame as pg

from theguest import (FUENTES, SONIDOS, TAM_FUENTE)


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()
        self.tipo1 = pg.font.Font(FUENTES['nasa'], TAM_FUENTE['1'])
        self.tipo2 = pg.font.Font(FUENTES['nasa'], TAM_FUENTE['2'])
        self.tipo3 = pg.font.Font(FUENTES['nasa'], TAM_FUENTE['3'])
        self.tipo4 = pg.font.Font(FUENTES['contraste'], TAM_FUENTE['3'])
        self.tipo5 = pg.font.Font(FUENTES['contraste'], TAM_FUENTE['4'])
        self.efecto_sonido = pg.mixer.Sound(SONIDOS['disparo'])
        self.imagenes = []
        for i in range(2):
            ruta_image = os.path.join(
                'resources', 'images', f'sonido{i}.png')
            image = pg.image.load(ruta_image)
            self.imagenes.append(image)
        self.tiem_ini_ton_toff = pg.time.get_ticks()
        self.ton_toff_visible = True

    def bucle_principal(self):
        pass

    def pintar_texto(self, mensaje, tipo, pos_x, pos_y, alineacion, color, fondo):
        if fondo == True:
            self.pantalla.blit(self.image, (0, 0))
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

    def comprobar_sonido(self):
        if self.sonido_activo:
            self.pantalla.blit(
                self.imagenes[0], (0, 0))
            self.musica = pg.mixer_music.set_volume(1.0)
            pg.mixer.Sound.set_volume(self.efecto_sonido, 1.0)
        else:
            self.pantalla.blit(
                self.imagenes[1], (0, 0))
            self.musica = pg.mixer_music.set_volume(0.0)
            pg.mixer.Sound.set_volume(self.efecto_sonido, 0.0)

    def ton_toff(self, tiempo_espera):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.tiem_ini_ton_toff >= tiempo_espera:
            self.ton_toff_visible = not self.ton_toff_visible
            self.tiem_ini_ton_toff = tiempo_actual

    def ton(self, tiempo_inicial, tiempo_espera):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - tiempo_inicial  > tiempo_espera:
            return True
        else:
            return False
        
    def toff(self, tiempo_inicial, tiempo_espera):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - tiempo_inicial  < tiempo_espera:
            return True
        else:
            return False
