import os
from datetime import date
import sqlite3


class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta

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

    def consultaConParametros(self, consulta, params):
        conexion, cursor = self.conectar()
        try:
            cursor.execute(consulta, params)
            conexion.commit()
        except Exception as ex:
            print(ex)
            conexion.rollback()

        self.desconectar(conexion)
