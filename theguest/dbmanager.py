import os
from datetime import date
import sqlite3


class DBManager:
    '''
    Clase para interactuar con la base de datos SQLite
    '''
    filename = 'records.db'
    file_dir = os.path.dirname(os.path.realpath(__file__))
    max_records = 10

    def __init__(self):

        self.data_path = os.path.join(
            os.path.dirname(self.file_dir),
            'data'
        )
        self.file_path = os.path.join(
            self.data_path, self.filename
        )
        self.check_records_file()

    def check_records_file(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
            print('No había directorio para datos, pero lo he creado!!!')
        if not os.path.exists(self.file_path):
            self.reset()

    def reset(self):
        self.game_records = []
        for i in range(self.max_records):
            self.game_records.append(['-----', 0])
        sql = 'CREATE TABLE "records" ( "id" INTEGER NOT NULL, "nombre" TEXT NOT NULL, "puntos" NUMERIC NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )'
        conexion, cursor = self.conectar()
        cursor.execute(sql)

    def conectar(self):
        conexion = sqlite3.connect(self.file_path)
        cursor = conexion.cursor()
        return conexion, cursor
