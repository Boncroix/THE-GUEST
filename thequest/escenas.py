import os


import pygame as pg


from .import (ALTO, ANCHO, AZUL, BLANCO, CENTRO_X, CENTRO_Y, FPS, HISTORIA, IMAGEN_PARTIDA, IMAGEN_PORTADA,
              INFO, INSTRUCCIONES, INTERVALO_PARPADEO_INFO, MARGEN_INF, MARGEN_IZQ, MUSICA_PARTIDA, MUSICA_PORTADA, FUENTE_NASA,
              FUENTE_CONTRAST, ROJO, TAM_FUENTE_1, TAM_FUENTE_2, TAM_FUENTE_3, TAM_FUENTE_4, VEL_FONDO_PARTIDA,
              VERDE)

from .entidades import IndicadorVida, Nave, Obstaculo


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
        self.image = pg.image.load(IMAGEN_PORTADA).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        pg.mixer.music.load(MUSICA_PORTADA)
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
        estado_teclas = pg.key.get_pressed()
        self.pintar_titulo()
        self.pintar_info()
        self.pintar_historia()
        self.mostrar_instrucciones(estado_teclas)
        self.mostrar_records(estado_teclas)

    def pintar_titulo(self):
        self.pintar_texto(['THE QUEST',], self.tipo4, CENTRO_X,
                          ALTO * 17/20, 'centro', VERDE, True)

    def pintar_info(self):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio >= INTERVALO_PARPADEO_INFO:
            self.parpadeo_visible = not self.parpadeo_visible
            self.ultimo_cambio = tiempo_actual
        if self.parpadeo_visible:
            self.pintar_texto(INFO, self.tipo3, CENTRO_X,
                              0, 'centro', BLANCO, False)

    def pintar_historia(self):
        self.pintar_texto(HISTORIA, self.tipo2, CENTRO_X,
                          ALTO * 11/20, 'centro', BLANCO, False)

    def mostrar_instrucciones(self, estado_teclas):
        if estado_teclas[pg.K_i]:
            self.pintar_texto(INSTRUCCIONES, self.tipo2, MARGEN_IZQ,
                              ALTO * 7/20, '', BLANCO, True)

    def mostrar_records(self, estado_teclas):
        if estado_teclas[pg.K_r]:
            self.pantalla.blit(self.image, (0, 0))

    def pintar_texto(self, txt, tipo, pos_x, pos_y, alineacion, color, fondo):
        if fondo == True:
            self.pantalla.blit(self.image, (0, 0))
        for linea in txt:
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


class Partida(Escena):
    def __init__(self, pantalla, dificultad, vidas):
        super().__init__(pantalla)
        self.image = pg.image.load(IMAGEN_PARTIDA).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.nave = Nave()
        self.obstaculos = pg.sprite.Group()
        self.dificultad = dificultad
        self.contador = 0
        self.crear_obstaculos()
        self.vidas = vidas
        self.indicador_vidas = pg.sprite.Group()
        self.crear_vidas(self.vidas)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena partida')
        pg.mixer.music.load(MUSICA_PARTIDA)
        pg.mixer.music.play(-1)
        salir = False
        self.pos_x = 0
        while not salir:
            self.reloj.tick(FPS)
            self.pintar_fondo()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
                    return 'salir', self.dificultad, self.vidas
            self.pintar_fondo()
            self.nave.update()
            self.pantalla.blit(self.nave.image, self.nave.rect)
            self.obstaculos.draw(self.pantalla)
            self.update_obstaculos()
            self.indicador_vidas.update()
            self.indicador_vidas.draw(self.pantalla)
            self.detectar_colision_nave()
            if self.colision:
                self.vidas -= 1
                if len(self.indicador_vidas) > 0:
                    self.restar_vida()
                    return 'partida', self.dificultad, self.vidas
                else:
                    return 'records', self.dificultad, self.vidas

            pg.display.flip()

    def pintar_fondo(self):
        x_relativa = self.pos_x % ANCHO
        self.pantalla.blit(self.image, (x_relativa - ANCHO, 0))
        if x_relativa < ANCHO:
            self.pantalla.blit(self.image, (x_relativa, 0))
        self.pos_x -= VEL_FONDO_PARTIDA

    def crear_obstaculos(self):
        for i in range(self.dificultad):
            obstaculo = Obstaculo(self.dificultad)
            self.obstaculos.add(obstaculo)

    def update_obstaculos(self):
        for obstaculo in self.obstaculos:
            obstaculo.update(self.obstaculos)
        if len(self.obstaculos) < self.dificultad - 3:
            self.contador += 1
            if self.contador % 2 == 0:
                self.dificultad += 1
            self.crear_obstaculos()

    def detectar_colision_nave(self):
        self.colision = pg.sprite.spritecollide(
            self.nave, self.obstaculos, True)

    def crear_vidas(self, vidas):
        separador = 5
        for vida in range(vidas):

            indicador = IndicadorVida()
            indicador.rect.x = indicador.rect.width * vida + MARGEN_IZQ + separador * vida
            indicador.rect.top = MARGEN_INF
            self.indicador_vidas.add(indicador)

    def restar_vida(self):
        self.indicador_vidas.sprites()[-1].kill()


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
