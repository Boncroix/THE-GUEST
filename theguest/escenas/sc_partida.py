import pygame as pg

from theguest import (ALTO, ANCHO, CENTRO_X, CENTRO_Y, COLORES, FPS, FUENTES, IMAGENES,
                      MARGEN_INF, MARGEN_IZQ, MARGEN_SUP, TAM_FUENTE, TIEMPO_NIVEL)

from theguest.entidades import IndicadorVida, Nave, Obstaculo, Planeta

from .sc_escena import Escena


class Partida(Escena):
    vel_fondo_partida = 1
    tiempo_parpadeo = 600
    pos_x_fondo = 0

    def __init__(self, pantalla, sonido_activo, marcador):
        super().__init__(pantalla)
        self.sonido_activo = sonido_activo
        self.marcador = marcador   
        self.image = pg.image.load(IMAGENES['partida']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.nave = Nave()
        self.planeta = Planeta()
        self.obstaculos = pg.sprite.Group()
        
        self.tiempo_nivel = pg.USEREVENT +2
        pg.time.set_timer(self.tiempo_nivel, TIEMPO_NIVEL)
        self.crear_obstaculos()

        self.cambio_nivel_activo = False
        self.colision = False
        
       
    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena partida')
        while True:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_TAB:
                    self.sonido_activo = not self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and self.cambio_nivel_activo:
                    self.marcador.subir_nivel()
                    return 'partida', self.sonido_activo
                if evento.type == pg.USEREVENT +2 and not self.colision:
                    self.cambio_nivel_activo = True
                if evento.type == pg.USEREVENT +3:
                    return 'partida', self.sonido_activo
                if evento.type == pg.USEREVENT +4:
                    return 'records', self.sonido_activo

            self.pintar_fondo()
            self.comprobar_sonido()
            self.pantalla.blit(self.nave.image, self.nave.rect)
            self.obstaculos.draw(self.pantalla)
            self.pintar_info()
            self.pantalla.blit(self.planeta.image, self.planeta.rect)
            self.gestion_ciclo()         

            pg.display.flip()

    def gestion_ciclo(self):
        if self.cambio_nivel_activo:
            self.update_obstaculos()
            self.planeta.update()
            self.nave.aterrizar_nave(self.planeta)
        elif self.colision:
            self.nave.explosion_nave()
            if self.toff(self.tiempo_ini_colision,FPS * 2):
                self.efecto_sonido.play()
            duracion_sonido = int(
                self.efecto_sonido.get_length() * 1000)
            if self.ton(self.tiempo_ini_colision, duracion_sonido):
                if self.marcador.vidas > 1:
                    self.marcador.restar_vida()
                    cambio_de_escena = pg.USEREVENT +3
                    pg.event.post(pg.event.Event(cambio_de_escena))
                else:
                    cambio_de_escena = pg.USEREVENT +4
                    pg.event.post(pg.event.Event(cambio_de_escena))
        else:
            self.tiempo_ini_colision = pg.time.get_ticks()
            self.nave.update()
            self.update_obstaculos()
            self.detectar_colision_nave()

    def pintar_fondo(self):
        x_relativa = self.pos_x_fondo % ANCHO
        self.pantalla.blit(self.image, (x_relativa - ANCHO, 0))
        if x_relativa < ANCHO:
            self.pantalla.blit(self.image, (x_relativa, 0))
        self.pos_x_fondo -= self.marcador.nivel
        pg.draw.line(self.pantalla, COLORES['blanco'],
                     (0, MARGEN_INF), (ANCHO, MARGEN_INF))
        pg.draw.line(self.pantalla, COLORES['blanco'],
                     (0, MARGEN_SUP), (ANCHO, MARGEN_SUP))

    def crear_obstaculos(self):
        for i in range(self.marcador.dificultad):
            obstaculo = Obstaculo(self.marcador.dificultad)
            self.obstaculos.add(obstaculo)

    def update_obstaculos(self):
        for obstaculo in self.obstaculos:
            if not self.cambio_nivel_activo:
                if obstaculo.update(self.obstaculos):
                    self.marcador.incrementar_puntos()
            else:
                obstaculo.update(self.obstaculos)
        if len(self.obstaculos) < self.marcador.dificultad and not self.cambio_nivel_activo:
            self.crear_obstaculos()

    def detectar_colision_nave(self):
        for obstaculo in self.obstaculos:
            self.colision = pg.sprite.collide_mask(self.nave, obstaculo)
            if self.colision:
                break


    def pintar_info(self):
        # Pintar Titulo
        self.pintar_texto(['The Guest',], self.tipo4, CENTRO_X,
                          0, 'centro', COLORES['blanco'], False)
        # Pintar instrucciones para continuar
        self.ton_toff(self.tiempo_parpadeo)
        if self.parpadeo_visible and self.cambio_nivel_activo:
            self.pintar_texto(['Nivel completado pulsar <ESPACIO> para continuar',], self.tipo2, CENTRO_X,
                              MARGEN_SUP, 'centro', COLORES['blanco'], False)
        self.marcador.pintar()

