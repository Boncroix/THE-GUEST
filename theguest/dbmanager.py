import os
from datetime import date
import sqlite3


class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta

    def reset(self):
        sql = 'CREATE TABLE "records" ( "id" INTEGER NOT NULL, "nombre" TEXT NOT NULL, "puntos" INTEGER NOT NULL, PRIMARY KEY("id") )'
        conexion, cursor = self.conectar()
        cursor.execute(sql)
        lista_records = []
        for cont in range(5):
            lista_records.append(('-----', 0))
            print(lista_records)
        for nombre, puntos in lista_records:
            sql = 'INSERT INTO records (nombre,puntos) VALUES (?,?)'
            parametros = nombre, puntos
            self.insertar(sql, parametros)

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
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

    def insertar(self, consulta, params):
        conexion, cursor = self.conectar()
        try:
            cursor.execute(consulta, params)
            conexion.commit()
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
