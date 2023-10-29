import pygame as pg

from .sc_escena import Escena

from theguest import (ALTO, ANCHO, CENTRO_X, CENTRO_Y, COLORES, FPS, FUENTES, IMAGENES,
                      MARGEN_INF, MARGEN_IZQ, MARGEN_SUP, TAM_FUENTE, TIEMPO_NIVEL)

from theguest.entidades import IndicadorVida, Nave, Obstaculo, Planeta


class Partida(Escena):
    VEL_FONDO_PARTIDA = 1
    tiempo_parpadeo = 600

    def __init__(self, pantalla, dificultad, vidas, puntos, nivel, sonido_activo):
        super().__init__(pantalla)
        self.dificultad = self.dificultad_inicial = dificultad
        self.vidas = vidas
        self.puntos = puntos
        self.nivel = nivel
        self.sonido_activo = sonido_activo
        self.image = pg.image.load(IMAGENES['partida']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.nave = Nave()
        self.planeta = Planeta()
        self.obstaculos = pg.sprite.Group()
        self.contador = 0
        self.crear_obstaculos()
        self.indicador_vidas = pg.sprite.Group()
        self.crear_vidas(self.vidas)
        self.pos_x_fondo = 0
        self.tiempo_inicial = pg.time.get_ticks()
        self.cambio_nivel_activo = False
        self.tiempo_nivel = pg.USEREVENT
        pg.time.set_timer(self.tiempo_nivel, TIEMPO_NIVEL)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena partida')
        while True:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.dificultad, self.vidas, self.puntos, self.nivel, self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_s:
                    self.sonido_activo = not self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and self.cambio_nivel_activo:
                    self.nivel += 1
                    return 'partida', self.dificultad, self.vidas, self.puntos, self.nivel, self.sonido_activo
                if evento.type == pg.USEREVENT and not self.colision:
                    self.cambio_nivel_activo = True
            self.pintar_fondo()
            self.comprobar_sonido()
            self.pantalla.blit(self.nave.image, self.nave.rect)
            self.obstaculos.draw(self.pantalla)
            self.indicador_vidas.update()
            self.indicador_vidas.draw(self.pantalla)
            self.pintar_info()
            self.pantalla.blit(self.planeta.image, self.planeta.rect)
            if self.cambio_nivel_activo:
                self.update_obstaculos()
                self.planeta.update()
                self.nave.aterrizar_nave(self.planeta)
            else:
                accion = self.detectar_colision_nave()
                if accion == 'partida':
                    return 'partida', self.dificultad_inicial, self.vidas, self.puntos, self.nivel, self.sonido_activo
                elif accion == 'records':
                    return 'records', self.dificultad, self.vidas, self.puntos, self.nivel, self.sonido_activo

            pg.display.flip()

    def pintar_fondo(self):
        x_relativa = self.pos_x_fondo % ANCHO
        self.pantalla.blit(self.image, (x_relativa - ANCHO, 0))
        if x_relativa < ANCHO:
            self.pantalla.blit(self.image, (x_relativa, 0))
        self.pos_x_fondo -= self.nivel
        pg.draw.line(self.pantalla, COLORES['blanco'],
                     (0, MARGEN_INF), (ANCHO, MARGEN_INF))
        pg.draw.line(self.pantalla, COLORES['blanco'],
                     (0, MARGEN_SUP), (ANCHO, MARGEN_SUP))

    def crear_obstaculos(self):
        for i in range(self.dificultad):
            obstaculo = Obstaculo(self.dificultad)
            self.obstaculos.add(obstaculo)

    def update_obstaculos(self):
        for obstaculo in self.obstaculos:
            if not self.cambio_nivel_activo:
                self.puntos += obstaculo.update(self.obstaculos)
            else:
                obstaculo.update(self.obstaculos)
        if len(self.obstaculos) < self.dificultad - 3 and not self.cambio_nivel_activo:
            self.contador += 1
            if self.contador % 2 == 0:
                self.dificultad += 1
            self.crear_obstaculos()

    def detectar_colision_nave(self):
        for obstaculo in self.obstaculos:
            self.colision = pg.sprite.collide_mask(self.nave, obstaculo)
            if self.colision:
                break
        if self.colision:
            tiempo_actual = pg.time.get_ticks()
            self.nave.explosion_nave()
            if tiempo_actual - self.tiempo_inicial1 < FPS * 2:
                self.efecto_sonido.play()
            duracion_sonido = int(
                self.efecto_sonido.get_length() * 1000)
            if tiempo_actual - self.tiempo_inicial1 >= duracion_sonido:
                if len(self.indicador_vidas) > 1:
                    self.vidas -= 1
                    self.indicador_vidas.sprites()[-1].kill()
                    return 'partida'
                else:
                    return 'records'
        else:
            self.tiempo_inicial1 = pg.time.get_ticks()
            self.nave.update()
            self.update_obstaculos()
            return 'continuar'

    def crear_vidas(self, vidas):
        for vida in range(vidas):
            indicador = IndicadorVida()
            separador = indicador.rect.width / 2
            indicador.rect.center = (indicador.rect.width * vida + MARGEN_IZQ + separador * vida + indicador.rect.width / 2,
                                     ALTO - (ALTO - MARGEN_INF) / 2)
            self.indicador_vidas.add(indicador)

    def pintar_info(self):
        # Pintar Puntos
        self.pintar_texto([str(self.puntos),], self.tipo3, MARGEN_IZQ,
                          0, '', COLORES['blanco'], False)
        # Pintar Nivel
        self.pintar_texto(['Nivel ' + str(self.nivel),], self.tipo3, ANCHO * 4/5,
                          0, '', COLORES['blanco'], False)
        # Pintar Titulo
        self.pintar_texto(['The Guest',], self.tipo4, CENTRO_X,
                          0, 'centro', COLORES['blanco'], False)
        # Pintar mejor jugador
        self.pintar_texto(['High Score' + str(self.nivel),], self.tipo3, CENTRO_X,
                          MARGEN_INF, '', COLORES['blanco'], False)
        # Pintar instrucciones para continuar
        self.temporizador(self.tiempo_inicial, self.tiempo_parpadeo)
        if self.parpadeo_visible and self.cambio_nivel_activo:
            self.pintar_texto(['Nivel completado pulsar <ESPACIO> para continuar',], self.tipo2, CENTRO_X,
                              MARGEN_SUP, 'centro', COLORES['blanco'], False)
