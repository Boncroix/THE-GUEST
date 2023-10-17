import os

# AJUSTES JUEGO
FPS = 30


# AJUSTES PANTALLA
ANCHO = 1200
ALTO = 800
CENTRO_Y = ALTO / 2
CENTRO_X = ANCHO / 2


# FUENTES
TAM_FUENTE_PEQ = int((ANCHO * ALTO) / 50000)
TAM_FUENTE_MED = int((ANCHO * ALTO) / 35000)
TAM_FUENTE_GRA = int((ANCHO * ALTO) / 8000)
RUTA_FUENTE = os.path.join('resources', 'fonts', 'CabinSketch-Bold.ttf')

# COLORES
ROJO = (99, 0, 0)
VERDE = (0, 99, 0)
AZUL = (0, 0, 99)
BLANCO = (255, 255, 255)


# HISTORIA
ruta_historia = os.path.join('data', 'historia.txt')
with open(ruta_historia, 'r') as contenido:
    HISTORIA = contenido.readlines()

# INFORMACIÓN PORTADA
INTERVALO_PARPADEO = 600

# AJUSTES PARTIDA
VELOCIDAD_FONDO_PARTIDA = 1

# AJUSTES NAVE
VELOCIDAD_NAVE = 10
AUMENTO_VELOCIDAD = 1
