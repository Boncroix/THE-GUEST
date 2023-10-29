import os

import pygame as pg

from theguest import (ALTO, ANCHO, CENTRO_X, COLORES, IMAGENES, MARGEN_IZQ)

from .sc_escena import Escena


class Portada(Escena):
    tiempo_parpadeo = 600

    def __init__(self, pantalla, sonido_activo):
        super().__init__(pantalla)
        self.sonido_activo = sonido_activo
        self.image = pg.image.load(IMAGENES['portada']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.tiempo_inicial = pg.time.get_ticks()

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena portada')
        while True:
            self.pintar_portada()
            self.comprobar_sonido()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    return 'partida', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_s:
                    self.sonido_activo = not self.sonido_activo

            pg.display.flip()

    def pintar_portada(self):
        estado_teclas = pg.key.get_pressed()
        self.pintar_titulo()
        self.pintar_info()
        self.pintar_historia()
        self.mostrar_instrucciones(estado_teclas)
        self.mostrar_records(estado_teclas)

    def pintar_titulo(self):
        self.pintar_texto(['THE QUEST',], self.tipo5, CENTRO_X,
                          ALTO * 16/20, 'centro', COLORES['verde'], True)

    def pintar_info(self):
        ruta_info = os.path.join('data', 'info.txt')
        with open(ruta_info, 'r', encoding='utf-8') as contenido:
            info = contenido.readlines()
        self.temporizador(self.tiempo_inicial, self.tiempo_parpadeo)
        if self.parpadeo_visible:
            self.pintar_texto(info, self.tipo2, CENTRO_X,
                              0, 'centro', COLORES['blanco'], False)

    def pintar_historia(self):
        ruta_historia = os.path.join('data', 'historia.txt')
        with open(ruta_historia, 'r', encoding='utf-8') as contenido:
            historia = contenido.readlines()
        self.pintar_texto(historia, self.tipo1, CENTRO_X,
                          ALTO * 10/20, 'centro', COLORES['blanco'], False)

    def mostrar_instrucciones(self, estado_teclas):
        ruta_instrucciones = os.path.join('data', 'instrucciones.txt')
        with open(ruta_instrucciones, 'r', encoding='utf-8') as contenido:
            instrucciones = contenido.readlines()
        if estado_teclas[pg.K_i]:
            self.pintar_texto(instrucciones, self.tipo1, MARGEN_IZQ,
                              ALTO * 7/20, '', COLORES['blanco'], True)

    def mostrar_records(self, estado_teclas):
        if estado_teclas[pg.K_r]:
            self.pantalla.blit(self.image, (0, 0))