import pygame as pg

from theguest import (ALTO, ANCHO, CENTRO_X, COLORES, FPS, IMAGENES,
                      MARGEN_INF, MARGEN_SUP, SONIDOS, TIEMPO_NIVEL)

from theguest.entidades import Nave, Nave1, Obstaculo, Planeta, Proyectil

from .sc_escena import Escena


class Partida(Escena):
    vel_fondo_partida = 1
    tiempo_parpadeo = 600
    pos_x_fondo = 0
    nivel_maximo = 10
    nivel_con_habilidades = 5

    def __init__(self, pantalla, sonido_activo, marcador):
        super().__init__(pantalla)
        self.sonido_activo = sonido_activo
        self.marcador = marcador
        self.image = pg.image.load(IMAGENES['partida']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.tiempo_nivel = pg.USEREVENT +2
        pg.time.set_timer(self.tiempo_nivel, TIEMPO_NIVEL)
        self.obstaculos = pg.sprite.Group()
        self.proyectiles = pg.sprite.Group()
        if self.marcador.nivel > self.nivel_con_habilidades:
            self.nave = Nave1()
        else:
            self.nave = Nave()
        self.planeta = Planeta()
        self.crear_obstaculos()
        self.cambio_nivel_activo = False
        self.colision = False
        self.disparar = False
        
    def bucle_principal(self):
        super().bucle_principal()
        while True:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_TAB:
                    self.sonido_activo = not self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and self.cambio_nivel_activo:
                    if self.marcador.nivel == self.nivel_maximo:
                        return 'records', self.sonido_activo
                    else:
                        self.marcador.subir_nivel()
                        return 'partida', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE and self.marcador.nivel > self.nivel_con_habilidades and self.marcador.disparos > 0:
                    self.crear_proyectil()
                if evento.type == pg.USEREVENT +2 and not self.colision:
                    self.cambio_nivel_activo = True
                if evento.type == pg.USEREVENT +3:
                    return 'partida', self.sonido_activo
                if evento.type == pg.USEREVENT +4:
                    return 'records', self.sonido_activo

            self.pintar_fondo()
            self.comprobar_sonido()
            self.pintar_info()                                     
            self.pantalla.blit(self.nave.image, self.nave.rect)
            self.obstaculos.draw(self.pantalla)
            self.pantalla.blit(self.planeta.image, self.planeta.rect)
            self.proyectiles.draw(self.pantalla)
            self.gestion_bucle()         

            pg.display.flip()

    def gestion_bucle(self):
        if self.cambio_nivel_activo:
            self.update_obstaculos()
            self.planeta.update()
            self.nave.aterrizar_nave(self.planeta)
            self.upddate_proyectil()
        elif self.colision:
            self.nave.explosion_nave()
            if self.toff(self.tiempo_ini_colision,FPS * 2):
                self.efecto_sonido = pg.mixer.Sound(SONIDOS['explosion'])
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
            self.detectar_colision_proyectil()
            if self.disparar and len(self.proyectiles) > 0:
                self.upddate_proyectil()

    def pintar_fondo(self):
        x_relativa = self.pos_x_fondo % ANCHO
        self.pantalla.blit(self.image, (x_relativa - ANCHO, 0))
        if x_relativa < ANCHO:
            self.pantalla.blit(self.image, (x_relativa, 0))
        self.pos_x_fondo -= 1
        pg.draw.line(self.pantalla, COLORES['blanco'],
                     (0, MARGEN_INF), (ANCHO, MARGEN_INF))
        pg.draw.line(self.pantalla, COLORES['blanco'],
                     (0, MARGEN_SUP), (ANCHO, MARGEN_SUP))
        
    def pintar_info(self):
        self.pintar_texto(['The Guest',], self.tipo4, CENTRO_X,
                          0, 'centro', COLORES['blanco'], False)
        
        self.ton_toff(self.tiempo_parpadeo)
        if self.ton_toff_visible and self.cambio_nivel_activo:
            self.pintar_texto(['Nivel completado pulsar <ESPACIO> para continuar',], self.tipo2, CENTRO_X,
                              MARGEN_SUP, 'centro', COLORES['blanco'], False)
            
        if self.colision and self.marcador.vidas < 2:
                self.pintar_texto(['GAME OVER',], self.tipo5, CENTRO_X,
                          ALTO * 1/3, 'centro', COLORES['rojo'], False)
                
        if self.cambio_nivel_activo and self.marcador.nivel == self.nivel_maximo:
            self.pintar_texto(['YOU WIN',], self.tipo5, CENTRO_X, ALTO * 1/3, 'centro', COLORES['verde'], False)
            
        self.marcador.pintar()

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
        
    def crear_proyectil(self):
        proyectil = Proyectil(self.nave)
        self.proyectiles.add(proyectil)
        self.disparar = True
        self.efecto_sonido = pg.mixer.Sound(SONIDOS['disparo'])
        self.efecto_sonido.play()
        self.marcador.restar_disparo()

    def upddate_proyectil(self):
        self.proyectiles.update(self.proyectiles)

    def detectar_colision_proyectil(self):
        colision = pg.sprite.groupcollide(self.proyectiles, self.obstaculos, True, True)
        if colision:
            self.efecto_sonido = pg.mixer.Sound(SONIDOS['impacto'])
            self.efecto_sonido.play()
            self.marcador.incrementar_puntos()
        
            
                






