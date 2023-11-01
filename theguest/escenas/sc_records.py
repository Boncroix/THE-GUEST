import os

import pygame as pg

from theguest import (ALTO, ANCHO, CENTRO_X, CENTRO_Y,
                      COLORES, IMAGENES, MARGEN_SUP)

from theguest.dbmanager import DBManager

from .sc_escena import Escena


class Records(Escena):
    filename = 'records.db'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    max_records = 5

    def __init__(self, pantalla, sonido_activo, puntos):
        super().__init__(pantalla)
        self.records = []
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
        pg.time.set_timer(self.indicador_activo, 300)
        self.consultar_records()
        self.separadores = []
        self.crear_lista_separadores()

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena records')
        self.entrada_texto = ''
        insertar_record = self.comprobar_puntuacion()
        while True:
            self.pintar_fondo()
            self.comprobar_sonido()
            self.pintar_records()
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
                if evento.type == pg.KEYDOWN and insertar_record:
                    if evento.key == pg.K_BACKSPACE:
                        self.entrada_texto = self.entrada_texto[:-1]
                    elif evento.key == pg.K_RETURN:
                        self.insertar_record(self.entrada_texto, self.puntos)
                        insertar_record = False
                    elif len(self.entrada_texto) < 9:
                        self.entrada_texto += evento.unicode
            if insertar_record:
                self.pintar_mi_puntuacion()
            else:
                salir, jugar_otra = self.finalizar_partida()
                if jugar_otra:
                    return 'portada', self.sonido_activo, self.puntos
                if salir:
                    return 'salir', self.sonido_activo, self.puntos

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
                          CENTRO_Y, 'centro', COLORES['blanco'], False)
        self.pintar_texto(self.separadores, self.tipo3, CENTRO_X,
                          CENTRO_Y, 'centro', COLORES['blanco'], False)
        self.pintar_texto(self.puntuaciones, self.tipo3, ANCHO * 2/3,
                          CENTRO_Y, 'centro', COLORES['blanco'], False)

    def finalizar_partida(self):
        mensajes = ('¿Jugamos Otra? S/N', self.indicador)
        self.pintar_texto(mensajes, self.tipo3, CENTRO_X,
                          MARGEN_SUP, 'centro', COLORES['blanco'], False)

        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_s]:
            self.puntos = 0
            return True, True
        if estado_teclas[pg.K_n]:
            return True, False
        return False, False

    def consultar_records(self):
        sql = 'SELECT nombre, puntos FROM records ORDER BY puntos DESC, id ASC'
        self.records = self.db.consultaSQL(sql)
        self.puntuaciones = []
        self.nombres = []
        for nombre, puntos in self.records:
            self.nombres.append(nombre)
            self.puntuaciones.append(puntos)

    def crear_lista_separadores(self):
        for i in self.nombres:
            self.separadores.append('---')

    def insertar_record(self, nombre, puntos):
        sql = 'INSERT INTO records (nombre,puntos) VALUES (?,?)'
        self.db.consultaConParametros(sql, (nombre, puntos))
        self.consultar_records()
