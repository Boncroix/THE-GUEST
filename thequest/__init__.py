import os

# AJUSTES JUEGO
FPS = 30


# AJUSTES PANTALLA
ANCHO = 1200
ALTO = 800
CENTRO_Y = ALTO / 2
CENTRO_X = ANCHO / 2
MARGEN = 20


# FUENTES
TAM_FUENTE_1 = int((ANCHO * ALTO) / 80000)
TAM_FUENTE_2 = int((ANCHO * ALTO) / 60000)
TAM_FUENTE_3 = int((ANCHO * ALTO) / 40000)
TAM_FUENTE_4 = int((ANCHO * ALTO) / 10000)
FUENTE_NASA = os.path.join('resources', 'fonts', 'nasa.otf')
FUENTE_CONTRAST = os.path.join('resources', 'fonts', 'contrast.ttf')

# COLORES
ROJO = (99, 0, 0)
VERDE = (0, 99, 0)
AZUL = (0, 0, 99)
BLANCO = (255, 255, 255)


# INFORMACIÓN
ruta_info = os.path.join('data', 'info.txt')
with open(ruta_info, 'r') as contenido:
    INFO = contenido.readlines()

# HISTORIA
ruta_historia = os.path.join('data', 'historia.txt')
with open(ruta_historia, 'r') as contenido:
    HISTORIA = contenido.readlines()

# INSTRUCCIONES
ruta_instrucciones = os.path.join('data', 'instrucciones.txt')
with open(ruta_instrucciones, 'r') as contenido:
    INSTRUCCIONES = contenido.readlines()

# INFORMACIÓN PORTADA
INTERVALO_PARPADEO_INFO = 600

# AJUSTES PARTIDA
VELOCIDAD_FONDO_PARTIDA = 1

# AJUSTES NAVE
VELOCIDAD_NAVE = 10
AUMENTO_VELOCIDAD = 1
