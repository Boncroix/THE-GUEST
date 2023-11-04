import os

import sqlite3


class DBManager:
    max_records = 6
    filename = 'records.db'
    file_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(self.file_dir), 'data')
        self.file_path = os.path.join(self.data_path, self.filename)
        self.check_records_file()

    def check_records_file(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        if not os.path.exists(self.file_path):
            self.crear_db()

    def crear_db(self):
        sql = 'CREATE TABLE "records" ( "id" INTEGER NOT NULL, "nombre" TEXT NOT NULL, "puntos" INTEGER NOT NULL, PRIMARY KEY("id") )'
        self.records = self.consultaSQL(sql)
        for cont in range(self.max_records):
            self.records.append(('-----', 0))
        for nombre, puntos in self.records:
            sql = 'INSERT INTO records (nombre,puntos) VALUES (?,?)'
            parametros = nombre, puntos
            self.consultaConParametros(sql, parametros)

    def conectar(self):
        conexion = sqlite3.connect(self.file_path)
        cursor = conexion.cursor()
        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

    def consultaSQL(self, consulta):
        conexion, cursor = self.conectar()
        try:
            cursor.execute(consulta)
            datos = cursor.fetchall()
            conexion.commit()
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
        return datos

    def consultaConParametros(self, consulta, params):
        conexion, cursor = self.conectar()
        try:
            cursor.execute(consulta, params)
            conexion.commit()
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)

    def borrar(self, id):
        consulta = 'DELETE FROM records WHERE id=?'
        conexion, cursor = self.conectar()
        try:
            cursor.execute(consulta, (id,))
            conexion.commit()
        except Exception as ex:
            conexion.rollback()

        self.desconectar(conexion)
