import os
from datetime import date
import sqlite3


class DBManager:
    filename = 'records.db'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    max_records = 10

    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(self.file_dir), 'data')
        self.file_path = os.path.join(self.data_path, self.filename)
        self.check_records_file()

    def check_records_file(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        if not os.path.exists(self.file_path):
            self.game_records = self.reset()

    def reset(self):
        sql = 'CREATE TABLE "records" ( "id" INTEGER NOT NULL, "nombre" TEXT NOT NULL, "puntos" NUMERIC NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )'
        conexion, cursor = self.conectar()
        cursor.execute(sql)
        lista_records = []
        for cont in range(self.max_records):
            lista_records.append(['-----', str(0)])
        for nombre, puntos in lista_records:
            sql = 'INSERT INTO records (nombre,puntos) VALUES (?,?)'
            parametros = nombre, puntos
            self.consultaConParametros(sql, parametros)
        return lista_records

    def conectar(self):
        conexion = sqlite3.connect(self.file_path)
        cursor = conexion.cursor()
        return conexion, cursor

    def desconectar(self, conexion):
        conexion.close()

    def consultaConParametros(self, consulta, params):
        conexion, cursor = self.conectar()

        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
