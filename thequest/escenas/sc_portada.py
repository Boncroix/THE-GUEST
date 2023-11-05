import os

import pygame as pg

from thequest import (ALTO, ANCHO, CENTRO_X, COLORES, IMAGENES, MARGEN_IZQ)

from .sc_escena import Escena


class Portada(Escena):
    tiempo_parpadeo = 600
    tiempo_cambio_escena = 15000

    def __init__(self, pantalla, sonido_activo):
        super().__init__(pantalla)
        self.sonido_activo = sonido_activo
        self.image = pg.image.load(IMAGENES['portada']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.temp_cambio_escena = pg.USEREVENT
        pg.time.set_timer(self.temp_cambio_escena, self.tiempo_cambio_escena)
        self.instrucciones_en_pantalla = False

    def bucle_principal(self):
        super().bucle_principal()
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    return 'partida', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_TAB:
                    self.sonido_activo = not self.sonido_activo
                if evento.type == pg.USEREVENT and not self.instrucciones_en_pantalla:
                    return 'records', self.sonido_activo
            self.pintar_portada()
            self.comprobar_sonido()
            pg.display.flip()

    def pintar_portada(self):
        estado_teclas = pg.key.get_pressed()
        self.pintar_titulo()
        self.pintar_info()
        self.pintar_historia()
        self.mostrar_instrucciones(estado_teclas)

    def pintar_titulo(self):
        self.pintar_texto(['THE QUEST',], self.tipo5, CENTRO_X,
                          ALTO * 16/20, 'centro', COLORES['blanco'], True)

    def pintar_info(self):
        ruta_info = os.path.join('resources', 'textos', 'info.txt')
        with open(ruta_info, 'r', encoding='utf-8') as contenido:
            info = contenido.readlines()
        self.ton_toff(self.tiempo_parpadeo)
        if self.ton_toff_visible:
            self.pintar_texto(info, self.tipo2, CENTRO_X,
                              0, 'centro', COLORES['blanco'], False)

    def pintar_historia(self):
        ruta_historia = os.path.join('resources', 'textos', 'historia.txt')
        with open(ruta_historia, 'r', encoding='utf-8') as contenido:
            historia = contenido.readlines()
        self.pintar_texto(historia, self.tipo1, CENTRO_X,
                          ALTO * 10/20, 'centro', COLORES['blanco'], False)

    def mostrar_instrucciones(self, estado_teclas):
        ruta_instrucciones = os.path.join(
            'resources', 'textos', 'instrucciones.txt')
        with open(ruta_instrucciones, 'r', encoding='utf-8') as contenido:
            instrucciones = contenido.readlines()
        if estado_teclas[pg.K_i]:
            self.instrucciones_en_pantalla = True
            self.pintar_texto(instrucciones, self.tipo1, MARGEN_IZQ,
                              ALTO * 5/20, '', COLORES['blanco'], True)
        else:
            self.instrucciones_en_pantalla = False
