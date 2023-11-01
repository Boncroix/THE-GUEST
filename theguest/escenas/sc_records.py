import os

import pygame as pg

from theguest import (ALTO, ANCHO, CENTRO_X, CENTRO_Y,
                      COLORES, DIFICULTAD_INI, FPS, IMAGENES, MARGEN_SUP)

from theguest.dbmanager import DBManager
from theguest.entidades import Obstaculo

from .sc_escena import Escena


class Records(Escena):
    filename = 'records.db'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    max_records = 6
    pos_y_records = ALTO
    vel_visu_indicador = 300
    tiempo_cambio_escena = 7000

    def __init__(self, pantalla, sonido_activo, puntos):
        super().__init__(pantalla)
        self.data_path = os.path.join(os.path.dirname(self.file_dir), 'data')
        self.file_path = os.path.join(self.data_path, self.filename)
        self.db = DBManager(self.file_path)
        self.check_records_file()
        self.sonido_activo = sonido_activo
        self.image = pg.image.load(IMAGENES['records']).convert()
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        self.puntos = puntos
        self.indicador = '-'
        self.indicador_activo = pg.USEREVENT
        pg.time.set_timer(self.indicador_activo, self.vel_visu_indicador)
        self.consultar_records()
        self.separadores = []
        self.crear_lista_separadores()
        self.temp_cambio_escena = False
        self.obstaculos = pg.sprite.Group()
        self.crear_obstaculos()

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena records')
        self.entrada_texto = ''
        insertar_record = self.comprobar_puntuacion()
        while True:
            self.reloj.tick(FPS)
            self.pintar_fondo()
            self.comprobar_sonido()
            self.pintar_records()
            self.update_obstaculos()
            self.obstaculos.draw(self.pantalla)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return 'salir', self.sonido_activo, self.puntos
                if evento.type == pg.KEYDOWN and evento.key == pg.K_TAB:
                    self.sonido_activo = not self.sonido_activo
                if evento.type == pg.USEREVENT:
                    if self.indicador == '-':
                        self.indicador = '  '
                    else:
                        self.indicador = '-'
                if evento.type == pg.USEREVENT + 1 and not insertar_record:
                    return 'portada', self.sonido_activo, self.puntos
                if evento.type == pg.KEYDOWN and insertar_record:
                    if evento.key == pg.K_BACKSPACE:
                        self.entrada_texto = self.entrada_texto[:-1]
                    elif evento.key == pg.K_RETURN:
                        self.crear_obstaculos()
                        self.insertar_borrar_record(
                            self.entrada_texto, self.puntos)
                        insertar_record = False
                    elif len(self.entrada_texto) < 9:
                        self.entrada_texto += evento.unicode
            if insertar_record:
                self.pintar_mi_puntuacion()
            else:
                self.finalizar_partida()
            pg.display.flip()

    def check_records_file(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        if not os.path.exists(self.file_path):
            self.crear_db()

    def crear_db(self):
        sql = 'CREATE TABLE "records" ( "id" INTEGER NOT NULL, "nombre" TEXT NOT NULL, "puntos" INTEGER NOT NULL, PRIMARY KEY("id") )'
        self.records = self.db.consultaSQL(sql)
        for cont in range(self.max_records):
            self.records.append(('-----', 0))
        for nombre, puntos in self.records:
            sql = 'INSERT INTO records (nombre,puntos) VALUES (?,?)'
            parametros = nombre, puntos
            self.db.consultaConParametros(sql, parametros)

    def pintar_fondo(self):
        self.pantalla.blit(self.image, (0, 0))

    def comprobar_puntuacion(self):
        return self.puntos > self.puntuaciones[-1]

    def pintar_mi_puntuacion(self):
        mensajes = ['INSERTA TU NOMBRE', str(self.entrada_texto) + self.indicador, str(
            self.puntos), 'Intro para insertar record']
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

    def finalizar_partida(self):
        self.pintar_texto(['THE GUEST'], self.tipo5, CENTRO_X,
                          MARGEN_SUP, 'centro', COLORES['blanco'], False)
        if not self.temp_cambio_escena:
            activo = pg.USEREVENT + 1
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
