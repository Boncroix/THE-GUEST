import os

# AJUSTES JUEGO
FPS = 30
DIFICULTAD_INI = 5
VIDAS = 3
HABILITAR_MOV_DER_IZQ = False

# AJUSTES PANTALLA
POSICIO = {
    'ancho': 1200,
    'alto': 800,
    'margen': 60
}

ANCHO = 1200
ALTO = 800
CENTRO_Y = ALTO / 2
CENTRO_X = ANCHO / 2
MARGEN_IZQ = 60
MARGEN_SUP = 60
MARGEN_INF = ALTO - 60

# TAMAÑO FUENTES ESCALADA SEGÚN LA PANTALLA
TAM_FUENTE = {
    '1': int((ANCHO * ALTO) / 60000),
    '2': int((ANCHO * ALTO) / 40000),
    '3': int((ANCHO * ALTO) / 20000),
    '4': int((ANCHO * ALTO) / 10000)
}

# RUTAS FUENTES
ruta1 = str(os.path.join('resources', 'fonts', 'nasa.otf'))
ruta2 = str(os.path.join('resources', 'fonts', 'contrast.ttf'))
FUENTE = {
    'nasa': ruta1,
    'contraste': ruta2
}


# RUTAS MUSICA
ruta1 = str(os.path.join(
            'resources', 'music', 'pista_portada.mp3'))
ruta2 = str(os.path.join(
            'resources', 'music', 'pista_partida.mp3'))
ruta3 = str(os.path.join(
            'resources', 'music', 'pista_records.mp3'))
MUSICA = {
    'portada': ruta1,
    'partida': ruta2,
    'records': ruta3
}

# COLORES
COLORES = {
    'azul': (0, 0, 99),
    'blanco': (255, 255, 255),
    'rojo': (99, 0, 0),
    'verde': (0, 99, 0)
}
