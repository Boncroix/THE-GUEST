import pygame as pg

from theguest import (ALTO, ANCHO, CENTRO_X, CENTRO_Y, COLORES,
                      DIFICULTAD_INI, FPS, IMAGENES, MARGEN_SUP)

from theguest.dbmanager import DBManager
from theguest.entidades import Obstaculo

from .sc_escena import Escena


class Records(Escena):
    pos_y_records = ALTO
    vel_visu_indicador = 300
    tiempo_cambio_escena = 8000
    max_text_name_record = 10

    def __init__(self, pantalla, sonido_activo, marcador):
        super().__init__(pantalla)
        self.sonido_activo = sonido_activo
        self.marcador = marcador
        self.image = pg.image.load(IMAGENES['records']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.db = DBManager()
        self.obstaculos = pg.sprite.Group()
        self.consultar_records()
        self.crear_lista_separadores()
        self.crear_obstaculos()
        self.indicador = '-'
        self.entrada_texto = ''
        self.temp_cambio_escena = False

    def bucle_principal(self):
        super().bucle_principal()
        self.insertar_record = self.comprobar_puntuacion()
        while True:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo
                if evento.type == pg.KEYDOWN and evento.key == pg.K_TAB:
                    self.sonido_activo = not self.sonido_activo
                if evento.type == pg.USEREVENT + 6 and not self.insertar_record:
                    return 'portada', self.sonido_activo
                if evento.type == pg.KEYDOWN and self.insertar_record:
                    if evento.key == pg.K_BACKSPACE:
                        self.entrada_texto = self.entrada_texto[:-1]
                    elif evento.key == pg.K_RETURN:
                        self.crear_obstaculos()
                        self.insertar_borrar_record(
                            self.entrada_texto, self.marcador.puntos)
                        self.insertar_record = False
                    elif len(self.entrada_texto) < self.max_text_name_record:
                        self.entrada_texto += evento.unicode

            self.pintar_fondo()
            self.update_obstaculos()
            self.obstaculos.draw(self.pantalla)
            self.comprobar_sonido()
            self.pintar_records()
            self.gestion_bucle()
            pg.display.flip()

    def gestion_bucle(self):
        if self.insertar_record:
            self.pintar_mi_puntuacion()
        else:
            self.cambio_de_escena()

    def pintar_fondo(self):
        self.pantalla.blit(self.image, (0, 0))

    def comprobar_puntuacion(self):
        return self.marcador.puntos > self.puntuaciones[-1]

    def pintar_mi_puntuacion(self):
        self.ton_toff(self.vel_visu_indicador)
        if self.ton_toff_visible:
            self.indicador = '-'
        else:
            self.indicador = ' '
        mensajes = ['INSERTA TU NOMBRE', str(self.entrada_texto) + self.indicador, str(
            self.marcador.puntos), 'Intro para insertar record']
        self.pintar_texto(mensajes, self.tipo3, CENTRO_X,
                          MARGEN_SUP, 'centro', COLORES['blanco'], False)

    def pintar_records(self):

        self.pintar_texto(self.nombres, self.tipo3, ANCHO * 1/3,
                          self.pos_y_records, 'centro', COLORES['blanco'], False)
        self.pintar_texto(self.separadores, self.tipo3, CENTRO_X,
                          self.pos_y_records, 'centro', COLORES['blanco'], False)
        self.pintar_texto(self.puntuaciones, self.tipo3, ANCHO * 2/3,
                          self.pos_y_records, 'centro', COLORES['blanco'], False)

        if self.pos_y_records > CENTRO_Y:
            self.pos_y_records -= 3
        else:
            self.pos_y_records == CENTRO_Y

    def cambio_de_escena(self):
        self.pintar_texto(['THE GUEST'], self.tipo5, CENTRO_X,
                          MARGEN_SUP, 'centro', COLORES['blanco'], False)
        if not self.temp_cambio_escena:
            activo = pg.USEREVENT + 6
            pg.time.set_timer(activo, self.tiempo_cambio_escena)
            self.temp_cambio_escena = True

    def consultar_records(self):
        sql = 'SELECT id, nombre, puntos FROM records ORDER BY puntos DESC, id ASC'
        self.records = self.db.consultaSQL(sql)
        self.id = []
        self.nombres = []
        self.puntuaciones = []

        for id, nombre, puntos in self.records:
            self.id.append(id)
            self.nombres.append(nombre)
            self.puntuaciones.append(puntos)

    def crear_lista_separadores(self):
        self.separadores = []
        for i in self.nombres:
            self.separadores.append('---')

    def insertar_borrar_record(self, nombre, puntos):
        sql = 'INSERT INTO records (nombre,puntos) VALUES (?,?)'
        self.db.consultaConParametros(sql, (nombre, puntos))
        self.db.borrar(self.id[-1])
        self.consultar_records()

    def crear_obstaculos(self):
        for i in range(DIFICULTAD_INI):
            obstaculo = Obstaculo(DIFICULTAD_INI)
            self.obstaculos.add(obstaculo)

    def update_obstaculos(self):
        for obstaculo in self.obstaculos:
            obstaculo.update(self.obstaculos)
