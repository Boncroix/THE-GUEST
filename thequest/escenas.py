import os


import pygame as pg


from .import (ALTO, ANCHO, AZUL, BLANCO, CENTRO_Y, FPS, HISTORIA, INFO, INSTRUCCIONES,
              INTERVALO_PARPADEO_INFO, MARGEN, FUENTE_NASA, FUENTE_CONTRAST,
              ROJO, TAM_FUENTE_1, TAM_FUENTE_2, TAM_FUENTE_3, TAM_FUENTE_4,
              VELOCIDAD_FONDO_PARTIDA, VERDE)

from .entidades import Nave


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        print('Metodo vacio bucle principal de escena')
        pass


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.tipo1 = pg.font.Font(FUENTE_NASA, TAM_FUENTE_1)
        self.tipo2 = pg.font.Font(FUENTE_NASA, TAM_FUENTE_2)
        self.tipo3 = pg.font.Font(FUENTE_NASA, TAM_FUENTE_3)
        self.tipo4 = pg.font.Font(FUENTE_CONTRAST, TAM_FUENTE_4)
        ruta_image = os.path.join('resources', 'images', 'portada.jpg')
        self.image = pg.image.load(ruta_image).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        ruta_musica = os.path.join('resources', 'music', 'pista_portada.mp3')
        pg.mixer.music.load(ruta_musica)
        pg.mixer.music.play(-1)
        self.parpadeo_visible = True
        self.ultimo_cambio = pg.time.get_ticks()

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena portada')
        salir = False
        while not salir:
            self.pintar_portada()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                    return 'salir'
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                    salir = True
                    return 'partida'

            pg.display.flip()

    def pintar_portada(self):
        # Pintar imagen de fondo
        self.pantalla.blit(self.image, (0, 0))
        self.pintar_titulo()
        self.pintar_informacion()
        self.pintar_historia()
        self.visualizar_instrucciones()
        self.visualizar_records()

    def pintar_titulo(self):
        texto = self.tipo4.render('THE QUEST', True, ROJO)
        pos_x = (ANCHO - texto.get_width()) / 2
        pos_y = ALTO * 6/7
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_informacion(self):
        pos_y = 0
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio >= INTERVALO_PARPADEO_INFO:
            self.parpadeo_visible = not self.parpadeo_visible
            self.ultimo_cambio = tiempo_actual
        if self.parpadeo_visible:
            for linea in INFO:
                texto = self.tipo3.render(linea[:-1], True, BLANCO)
                pos_x = (ANCHO - texto.get_width()) / 2
                self.pantalla.blit(texto, (pos_x, pos_y))
                pos_y += texto.get_height()

    def pintar_historia(self):
        pos_y = CENTRO_Y
        for linea in HISTORIA:
            texto = self.tipo2.render(linea[:-1], True, BLANCO)
            pos_x = (ANCHO - texto.get_width()) / 2
            pos_y += texto.get_height()
            self.pantalla.blit(texto, (pos_x, pos_y))

    def visualizar_instrucciones(self):
        pos_y = ALTO * 1/3
        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_i]:
            # Pintar imagen de fondo
            self.pantalla.blit(self.image, (0, 0))
            for linea in INSTRUCCIONES:
                texto = self.tipo2.render(linea[:-1], True, BLANCO)
                pos_x = MARGEN
                pos_y += texto.get_height()
                self.pantalla.blit(texto, (pos_x, pos_y))

    def visualizar_records(self):
        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_r]:
            # Pintar imagen de fondo
            self.pantalla.blit(self.image, (0, 0))


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta_image = os.path.join('resources', 'images', 'partida.jpg')
        self.image = pg.image.load(ruta_image).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.ruta_musica = os.path.join('resources', 'music', 'pista0.mp3')
        self.nave = Nave()

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena partida')
        pg.mixer.music.load(self.ruta_musica)
        pg.mixer.music.play(-1)
        salir = False
        self.pos_x = 0
        while not salir:
            self.reloj.tick(FPS)
            self.pintar_fondo()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                    return 'salir'
            self.pintar_fondo()
            self.nave.update()
            self.pantalla.blit(self.nave.image, self.nave.rect)
            pg.display.flip()

    def pintar_fondo(self):
        x_relativa = self.pos_x % ANCHO
        self.pantalla.blit(self.image, (x_relativa - ANCHO, 0))
        if x_relativa < ANCHO:
            self.pantalla.blit(self.image, (x_relativa, 0))
        self.pos_x -= VELOCIDAD_FONDO_PARTIDA


class Records(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena records')
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((0, 0, 99))
            pg.display.flip()
